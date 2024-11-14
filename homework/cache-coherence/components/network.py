from itertools import zip_longest
from m5.objects import SimpleNetwork, Switch, SimpleExtLink, SimpleIntLink


class L1L2ClusterTree(SimpleNetwork):
    """A simple tree network. This doesn't not use garnet.

    Assumptions:
      - The number of L1 controllers is the same as the number of L2
        controllers.
      - There is one directory

    Each L2 bank is paired with an L1 controller. The order of the controllers
    in the two lists determines the pairing.
    The L2s are connected to a single router (crossbar).
    The directory is then also connected to this router.
    """

    _intLinkId = 0
    _extLinkId = 0
    _routerId = 0

    @classmethod
    def _getIntLinkId(cls):
        cls._intLinkId += 1
        return cls._intLinkId - 1

    @classmethod
    def _getExtLinkId(cls):
        cls._extLinkId += 1
        return cls._extLinkId - 1

    @classmethod
    def _getRouterId(cls):
        cls._routerId += 1
        return cls._routerId - 1

    def __init__(self, ruby_system, xbar_latency):
        super().__init__()
        self.netifs = []
        self._xbar_latency = xbar_latency

        # TODO: These should be in a base class
        # https://gem5.atlassian.net/browse/GEM5-1039
        self.ruby_system = ruby_system

    def connectControllers(self, l1_ctrls, l2_ctrls, dir_ctrl):
        """Connect all of the controllers to routers and connect the routers
        together as specified in the docstring of the class.
        Assumptions:
        - The number of L1 controllers is the same as the number of L2
            controllers.
        - There is one directory
        """
        # NOTE: Hack for SE mode with a `- 1` here and the first two L1s
        # are connected to a single L2
        assert len(l1_ctrls) - 1 == len(l2_ctrls)

        routers = []
        int_links = []
        ext_links = []

        self.xbar = Switch(router_id=self._getRouterId())
        routers.append(self.xbar)

        # for every l1/l2 pair create a connection. Then, connect this to a
        # xbar.
        for i, (l1, l2) in enumerate(zip(l1_ctrls[1:], l2_ctrls)):
            # Create the router/switch
            l1_switch = Switch(router_id=self._getRouterId())
            setattr(self, f"l1_switch_{i}", l1_switch)
            routers.append(getattr(self, f"l1_switch_{i}"))
            # Connect the l1
            setattr(
                self,
                f"l1_link_{i}",
                SimpleExtLink(
                    link_id=self._getExtLinkId(),
                    ext_node=l1,
                    int_node=l1_switch,
                ),
            )
            ext_links.append(getattr(self, f"l1_link_{i}"))

            # Add router for L2
            l2_switch = Switch(router_id=self._getRouterId())
            setattr(self, f"l2_switch_{i}", l2_switch)
            routers.append(getattr(self, f"l2_switch_{i}"))
            # Connect the L2
            setattr(
                self,
                f"l2_link_{i}",
                SimpleExtLink(
                    link_id=self._getExtLinkId(),
                    ext_node=l2,
                    int_node=l2_switch,
                ),
            )
            ext_links.append(getattr(self, f"l2_link_{i}"))

            # Connect L1 router to L2 router
            setattr(
                self,
                f"l1_l2_link{i}",
                SimpleIntLink(
                    link_id=self._getIntLinkId(),
                    src_node=l1_switch,
                    dst_node=l2_switch,
                ),
            )
            int_links.append(getattr(self, f"l1_l2_link{i}"))
            setattr(
                self,
                f"l2_l1_link{i}",
                SimpleIntLink(
                    link_id=self._getIntLinkId(),
                    src_node=l2_switch,
                    dst_node=l1_switch,
                ),
            )
            int_links.append(getattr(self, f"l2_l1_link{i}"))

            # Connect the L2 router to the xbar
            setattr(
                self,
                f"l2_xbar_link{i}",
                SimpleIntLink(
                    link_id=self._getIntLinkId(),
                    src_node=l2_switch,
                    dst_node=self.xbar,
                    latency=self._xbar_latency,
                ),
            )
            int_links.append(getattr(self, f"l2_xbar_link{i}"))
            setattr(
                self,
                f"xbar_l2_link{i}",
                SimpleIntLink(
                    link_id=self._getIntLinkId(),
                    src_node=self.xbar,
                    dst_node=l2_switch,
                    latency=self._xbar_latency,
                ),
            )
            int_links.append(getattr(self, f"xbar_l2_link{i}"))

        # Connect the directory to the xbar
        self.dir_ext_link = SimpleExtLink(
            link_id=self._getExtLinkId(), ext_node=dir_ctrl, int_node=self.xbar
        )
        ext_links.append(self.dir_ext_link)

        # HACK: Connect first L1 directory to the xbar
        self.hack_ext_link = SimpleExtLink(
            link_id=self._getExtLinkId(),
            ext_node=l1_ctrls[0],
            int_node=self.xbar,
        )
        ext_links.append(self.hack_ext_link)

        self.ext_links = ext_links
        self.int_links = int_links
        self.routers = routers
