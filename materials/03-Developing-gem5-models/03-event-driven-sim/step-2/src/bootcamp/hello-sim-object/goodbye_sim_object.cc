#include "bootcamp/hello-sim-object/goodbye_sim_object.hh"

#include "base/trace.hh"
#include "debug/GoodByeExampleFlag.hh"

namespace gem5
{

GoodByeSimObject::GoodByeSimObject(const GoodByeSimObjectParams& params):
    SimObject(params),
    nextGoodByeEvent([this]() { processNextGoodByeEvent(); }, name() + ".nextGoodByeEvent" )
{}

void
GoodByeSimObject::sayGoodBye() {
    panic_if(nextGoodByeEvent.scheduled(), "GoodByeSimObject::sayGoodBye called while nextGoodByeEvent is scheduled!");
    schedule(nextGoodByeEvent, curTick() + 500);
}

void
GoodByeSimObject::processNextGoodByeEvent()
{
    DPRINTF(GoodByeExampleFlag, "%s: GoodBye from GoodByeSimObejct::processNextGoodByeEvent!\n", __func__);
}

} // namespace gem5
