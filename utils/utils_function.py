
class UtilsFunction:
    @staticmethod
    def to_lower(value):
        try:
            return value.lower() if isinstance(value, str) else value
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()