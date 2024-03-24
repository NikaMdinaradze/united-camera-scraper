from pydantic import BaseModel, field_validator, ValidationError

class CameraPreview(BaseModel):
    brand: str
    model: str
    price: str | float
    detailed_link: str
    category: str

    @field_validator("price")
    def parse_float_price(cls, value):
        price_str = str(value).replace('$', '').replace(',', '')
        try:
            return float(price_str)
        except ValueError:
            return "Not Available"

    @classmethod
    def validate_dict(cls, data: dict) -> dict:
        try:
            validated_dict = cls.parse_obj(data).dict()
            return validated_dict
        except ValidationError as e:
            error_messages = []
            for error in e.errors():
                error_messages.append(f"{error['loc']}: {error['msg']}")
            raise ValueError(f"Validation error(s) occurred: {', '.join(error_messages)}."
                             f"Data: {data}")
