import contextlib
import can

timings = set()
for sample_point in range(50, 100):
    with contextlib.suppress(ValueError):
        timings.add(
            can.BitTiming.from_sample_point(
                f_clock=8_000_000,
                bitrate=250_000,
                sample_point=sample_point,
            )
        )

for timing in sorted(timings, key=lambda x: x.sample_point):
    print(timing)