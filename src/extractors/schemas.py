from pydantic import BaseModel, field_validator

class BasePreview(BaseModel):
    brand: str
    model: str
    price: float
    detailed_link: str
    category: str

    @field_validator("price")
    def parse_float_price(cls, value):
        try:
            price_str = str(value).replace('$', '').replace(',', '')
            return float(price_str)
        except ValueError:
            raise ValueError(f"Invalid price format: {value}. Price must be a number.")

