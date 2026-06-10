from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Lithology(Base):
    __tablename__ = "lithology"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="岩性名称")
    description = Column(Text, comment="描述")
    created_at = Column(DateTime, server_default=func.now())
    
    thin_sections = relationship("ThinSection", back_populates="lithology")


class Drawer(Base):
    __tablename__ = "drawer"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), unique=True, nullable=False, comment="抽屉位置")
    capacity = Column(Integer, default=50, comment="容量")
    description = Column(Text, comment="描述")
    created_at = Column(DateTime, server_default=func.now())
    
    thin_sections = relationship("ThinSection", back_populates="drawer")


class CourseBatch(Base):
    __tablename__ = "course_batch"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="课程批次名称")
    course_name = Column(String(100), comment="课程名称")
    semester = Column(String(50), comment="学期")
    year = Column(Integer, comment="年份")
    created_at = Column(DateTime, server_default=func.now())
    
    borrow_records = relationship("BorrowRecord", back_populates="course_batch")
    reservations = relationship("BorrowReservation", back_populates="course_batch")


class Borrower(Base):
    __tablename__ = "borrower"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="姓名")
    student_id = Column(String(50), unique=True, comment="学号/工号")
    department = Column(String(100), comment="院系")
    phone = Column(String(20), comment="联系电话")
    created_at = Column(DateTime, server_default=func.now())
    
    borrow_records = relationship("BorrowRecord", back_populates="borrower")
    reservations = relationship("BorrowReservation", back_populates="borrower")


class ThinSection(Base):
    __tablename__ = "thin_section"
    
    id = Column(Integer, primary_key=True, index=True)
    section_no = Column(String(50), unique=True, nullable=False, comment="薄片编号")
    name = Column(String(100), comment="薄片名称")
    lithology_id = Column(Integer, ForeignKey("lithology.id"), comment="岩性ID")
    drawer_id = Column(Integer, ForeignKey("drawer.id"), comment="抽屉位置ID")
    thickness = Column(String(50), comment="厚度")
    preparation_date = Column(Date, comment="制备日期")
    label_status = Column(String(20), default="完好", comment="标签状态：完好/磨损/缺失")
    status = Column(String(20), default="在库", comment="状态：在库/借出/维修中")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    lithology = relationship("Lithology", back_populates="thin_sections")
    drawer = relationship("Drawer", back_populates="thin_sections")
    borrow_records = relationship("BorrowRecord", back_populates="thin_section")
    reservations = relationship("BorrowReservation", back_populates="thin_section")


class BorrowReservation(Base):
    __tablename__ = "borrow_reservation"
    
    id = Column(Integer, primary_key=True, index=True)
    thin_section_id = Column(Integer, ForeignKey("thin_section.id"), nullable=False, comment="薄片ID")
    borrower_id = Column(Integer, ForeignKey("borrower.id"), nullable=False, comment="借阅人ID")
    course_batch_id = Column(Integer, ForeignKey("course_batch.id"), comment="课程批次ID")
    purpose = Column(String(200), comment="预约用途")
    reservation_date = Column(Date, comment="预约日期")
    expected_return_date = Column(Date, comment="预计归还日期")
    remarks = Column(Text, comment="申请备注")
    
    status = Column(String(20), default="待审批", comment="预约状态：待审批/已通过/已拒绝/已取消/已转借出")
    approval_remarks = Column(Text, comment="审批备注")
    approved_by = Column(String(100), comment="审批人")
    approved_at = Column(DateTime, comment="审批时间")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    thin_section = relationship("ThinSection", back_populates="reservations")
    borrower = relationship("Borrower", back_populates="reservations")
    course_batch = relationship("CourseBatch", back_populates="reservations")


class BorrowRecord(Base):
    __tablename__ = "borrow_record"
    
    id = Column(Integer, primary_key=True, index=True)
    thin_section_id = Column(Integer, ForeignKey("thin_section.id"), nullable=False, comment="薄片ID")
    borrower_id = Column(Integer, ForeignKey("borrower.id"), nullable=False, comment="借阅人ID")
    course_batch_id = Column(Integer, ForeignKey("course_batch.id"), comment="课程批次ID")
    purpose = Column(String(200), comment="用途")
    borrow_quantity = Column(Integer, default=1, comment="借出数量")
    appearance_grade = Column(String(20), comment="借出时外观等级")
    expected_return_date = Column(Date, comment="预计归还日期")
    borrow_date = Column(Date, comment="借出日期")
    remarks = Column(Text, comment="借出备注")
    
    is_returned = Column(Boolean, default=False, comment="是否已归还")
    return_date = Column(Date, comment="实际归还日期")
    has_crack = Column(Boolean, default=False, comment="是否有裂纹")
    has_stain = Column(Boolean, default=False, comment="是否有污渍")
    label_worn = Column(Boolean, default=False, comment="标签是否磨损")
    reinspection_result = Column(String(20), comment="复检结果")
    return_remarks = Column(Text, comment="归还备注")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    thin_section = relationship("ThinSection", back_populates="borrow_records")
    borrower = relationship("Borrower", back_populates="borrow_records")
    course_batch = relationship("CourseBatch", back_populates="borrow_records")
