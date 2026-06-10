from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field
from datetime import date, datetime

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    code: int = Field(default=200, description="响应码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")


class LithologyBase(BaseModel):
    name: str
    description: Optional[str] = None


class LithologyCreate(LithologyBase):
    pass


class LithologyUpdate(LithologyBase):
    name: Optional[str] = None


class Lithology(LithologyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DrawerBase(BaseModel):
    location: str
    capacity: Optional[int] = 50
    description: Optional[str] = None


class DrawerCreate(DrawerBase):
    pass


class DrawerUpdate(DrawerBase):
    location: Optional[str] = None


class Drawer(DrawerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourseBatchBase(BaseModel):
    name: str
    course_name: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[int] = None


class CourseBatchCreate(CourseBatchBase):
    pass


class CourseBatchUpdate(CourseBatchBase):
    name: Optional[str] = None


class CourseBatch(CourseBatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BorrowerBase(BaseModel):
    name: str
    student_id: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None


class BorrowerCreate(BorrowerBase):
    pass


class BorrowerUpdate(BorrowerBase):
    name: Optional[str] = None


class Borrower(BorrowerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ThinSectionBase(BaseModel):
    section_no: str
    name: Optional[str] = None
    lithology_id: Optional[int] = None
    drawer_id: Optional[int] = None
    thickness: Optional[str] = None
    preparation_date: Optional[date] = None
    label_status: Optional[str] = "完好"
    status: Optional[str] = "在库"
    remarks: Optional[str] = None


class ThinSectionCreate(ThinSectionBase):
    pass


class ThinSectionUpdate(ThinSectionBase):
    section_no: Optional[str] = None


class ThinSection(ThinSectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    lithology: Optional[Lithology] = None
    drawer: Optional[Drawer] = None

    class Config:
        from_attributes = True


class BorrowRecordBase(BaseModel):
    thin_section_id: int
    borrower_id: int
    course_batch_id: Optional[int] = None
    purpose: Optional[str] = None
    borrow_quantity: Optional[int] = 1
    appearance_grade: Optional[str] = None
    expected_return_date: date
    borrow_date: date
    remarks: Optional[str] = None


class BorrowRecordCreate(BorrowRecordBase):
    pass


class BorrowRecordReturn(BaseModel):
    return_date: date
    has_crack: bool = False
    has_stain: bool = False
    label_worn: bool = False
    reinspection_result: str
    return_remarks: Optional[str] = None


class BorrowRecord(BorrowRecordBase):
    id: int
    is_returned: bool = False
    return_date: Optional[date] = None
    has_crack: Optional[bool] = False
    has_stain: Optional[bool] = False
    label_worn: Optional[bool] = False
    reinspection_result: Optional[str] = None
    return_remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    thin_section: Optional[ThinSection] = None
    borrower: Optional[Borrower] = None
    course_batch: Optional[CourseBatch] = None

    class Config:
        from_attributes = True


class OverdueItem(BaseModel):
    borrow_id: int
    section_no: str
    section_name: Optional[str]
    borrower_name: str
    expected_return_date: date
    overdue_days: int


class DamageReinspectionItem(BaseModel):
    borrow_id: int
    section_no: str
    section_name: Optional[str]
    borrower_name: str
    damage_type: str
    return_date: date


class MissingLabelItem(BaseModel):
    section_id: int
    section_no: str
    section_name: Optional[str]
    label_status: str
    last_borrow_date: Optional[date]


class DamageCourseItem(BaseModel):
    course_batch_id: int
    course_batch_name: str
    total_borrow_count: int
    damage_count: int
    damage_rate: float


class DrawerUsageItem(BaseModel):
    drawer_id: int
    location: str
    capacity: int
    used_count: int
    usage_rate: float


class BorrowReservationBase(BaseModel):
    thin_section_id: int
    borrower_id: int
    course_batch_id: Optional[int] = None
    purpose: Optional[str] = None
    reservation_date: date
    expected_return_date: date
    remarks: Optional[str] = None


class BorrowReservationCreate(BorrowReservationBase):
    pass


class BorrowReservationApprove(BaseModel):
    approval_remarks: Optional[str] = None
    approved_by: Optional[str] = None


class BorrowReservationReject(BaseModel):
    approval_remarks: str
    approved_by: Optional[str] = None


class BorrowReservationCancel(BaseModel):
    approval_remarks: Optional[str] = None


class BorrowReservationConvert(BaseModel):
    borrow_date: date
    appearance_grade: Optional[str] = None
    borrow_quantity: Optional[int] = 1


class BorrowReservation(BorrowReservationBase):
    id: int
    status: str
    approval_remarks: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    thin_section: Optional[ThinSection] = None
    borrower: Optional[Borrower] = None
    course_batch: Optional[CourseBatch] = None

    class Config:
        from_attributes = True


class PageResult(BaseModel, Generic[T]):
    total: int
    items: List[T]
