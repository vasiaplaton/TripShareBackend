
class ADCBetError(Exception):
    """Общее исключение при ошибке c ADC Bet App"""


class ReqError(ADCBetError):
    """Исключение, выбрасываемое при ошибке в запросе"""


class NotFoundError(ReqError):
    """Не нашли что-то где-то"""