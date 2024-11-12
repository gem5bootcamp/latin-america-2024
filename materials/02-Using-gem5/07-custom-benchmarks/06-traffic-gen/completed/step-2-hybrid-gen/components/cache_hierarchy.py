from m5.params import NULL

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.utils.override import overrides


class MyPrivateL1SharedL2CacheHierarchy(PrivateL1SharedL2CacheHierarchy):
    def __init__(
        self,
        l1d_size="16KiB",
        l1i_size="16KiB",
        l2_size="256KiB",
    ) -> None:
        super().__init__(
            l1d_size=l1d_size,
            l1i_size=l1i_size,
            l2_size=l2_size,
        )

    @overrides(PrivateL1SharedL2CacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        super().incorporate_cache(board)
        for cache in self.l1icaches:
            cache.prefetcher = NULL
        for cache in self.l1dcaches:
            cache.prefetcher = NULL
        self.l2cache.prefetcher = NULL
