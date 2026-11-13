class Supplier:
    """A supplier that provides products. Exists independently of any Product."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id: str = str(supplier_id)
        self.name: str = name
        self.contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    def display_information(self) -> None:
        print(f"Supplier ID: {self._supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Supplier Email: {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self._supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }
