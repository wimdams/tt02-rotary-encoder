import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


segmentsforward = [ 63, 6, 91, 79, 102, 109, 125, 7, 127, 111 ]
segmentsbackward = [ 63, 111, 127, 7, 125, 109, 102, 79, 91, 6 ]

@cocotb.test()
async def rotary_encoder(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    dut.A.value = 0
    dut.B.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("Rotating forward")
    for i in range(10):
        dut.A.value = 0
        dut._log.info("check segment {}".format(i))
        assert int(dut.segments.value) == segmentsforward[i]
        await ClockCycles(dut.clk, 100)
        dut.A.value = 1
        await ClockCycles(dut.clk, 100)

    dut._log.info("Rotating backward")
    dut.B.value = 1
    for i in range(10):
        dut.A.value = 0
        dut._log.info("check segment {}".format(i))
        assert int(dut.segments.value) == segmentsbackward[i]
        await ClockCycles(dut.clk, 100)
        dut.A.value = 1
        await ClockCycles(dut.clk, 100)
