from dataclasses import dataclass


@dataclass(frozen=True)
class RequestParameters:
    reverse: bool
    speed: int
    keep_pitch: bool
    stereo_shift: int

    def __post_init__(self):
        if self.speed < 50 or self.speed > 200:
            raise ValueError()
        if self.stereo_shift < 0 or self.stereo_shift > 4:
            raise ValueError()

    @staticmethod
    def parse(args):
        return RequestParameters(
            reverse=args.get('reverse', 'false') == 'true',
            speed=int(args.get('speed', '100')),
            keep_pitch=args.get('keepPitch', 'false') == 'true',
            stereo_shift=int(args.get('stereoShift', '0')),
        )
