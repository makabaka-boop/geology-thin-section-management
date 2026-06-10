from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, Integer
from datetime import date, datetime
from typing import Optional, List

from database import engine, get_db, Base
from models import Lithology, Drawer, CourseBatch, Borrower, ThinSection, BorrowRecord, BorrowReservation, MaintenanceRecord
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="地学教学室矿样薄片管理系统", version="1.0.0")


def success_response(data=None, message="success"):
    return {"code": 200, "message": message, "data": data}


def error_response(code=400, message="error", data=None):
    return {"code": code, "message": message, "data": data}


@app.post("/api/lithology", response_model=schemas.ResponseModel[schemas.Lithology])
def create_lithology(lithology: schemas.LithologyCreate, db: Session = Depends(get_db)):
    existing = db.query(Lithology).filter(Lithology.name == lithology.name).first()
    if existing:
        return error_response(400, "岩性名称已存在")
    db_lithology = Lithology(**lithology.model_dump())
    db.add(db_lithology)
    db.commit()
    db.refresh(db_lithology)
    return success_response(db_lithology)


@app.get("/api/lithology", response_model=schemas.ResponseModel[List[schemas.Lithology]])
def list_lithology(db: Session = Depends(get_db)):
    lithologies = db.query(Lithology).all()
    return success_response(lithologies)


@app.get("/api/lithology/{lithology_id}", response_model=schemas.ResponseModel[schemas.Lithology])
def get_lithology(lithology_id: int, db: Session = Depends(get_db)):
    lithology = db.query(Lithology).filter(Lithology.id == lithology_id).first()
    if not lithology:
        return error_response(404, "岩性不存在")
    return success_response(lithology)


@app.put("/api/lithology/{lithology_id}", response_model=schemas.ResponseModel[schemas.Lithology])
def update_lithology(lithology_id: int, lithology: schemas.LithologyUpdate, db: Session = Depends(get_db)):
    db_lithology = db.query(Lithology).filter(Lithology.id == lithology_id).first()
    if not db_lithology:
        return error_response(404, "岩性不存在")
    if lithology.name:
        existing = db.query(Lithology).filter(Lithology.name == lithology.name, Lithology.id != lithology_id).first()
        if existing:
            return error_response(400, "岩性名称已存在")
    for key, value in lithology.model_dump(exclude_unset=True).items():
        setattr(db_lithology, key, value)
    db.commit()
    db.refresh(db_lithology)
    return success_response(db_lithology)


@app.delete("/api/lithology/{lithology_id}", response_model=schemas.ResponseModel)
def delete_lithology(lithology_id: int, db: Session = Depends(get_db)):
    db_lithology = db.query(Lithology).filter(Lithology.id == lithology_id).first()
    if not db_lithology:
        return error_response(404, "岩性不存在")
    db.delete(db_lithology)
    db.commit()
    return success_response(None, "删除成功")


@app.post("/api/drawer", response_model=schemas.ResponseModel[schemas.Drawer])
def create_drawer(drawer: schemas.DrawerCreate, db: Session = Depends(get_db)):
    existing = db.query(Drawer).filter(Drawer.location == drawer.location).first()
    if existing:
        return error_response(400, "抽屉位置已存在")
    db_drawer = Drawer(**drawer.model_dump())
    db.add(db_drawer)
    db.commit()
    db.refresh(db_drawer)
    return success_response(db_drawer)


@app.get("/api/drawer", response_model=schemas.ResponseModel[List[schemas.Drawer]])
def list_drawer(db: Session = Depends(get_db)):
    drawers = db.query(Drawer).all()
    return success_response(drawers)


@app.get("/api/drawer/{drawer_id}", response_model=schemas.ResponseModel[schemas.Drawer])
def get_drawer(drawer_id: int, db: Session = Depends(get_db)):
    drawer = db.query(Drawer).filter(Drawer.id == drawer_id).first()
    if not drawer:
        return error_response(404, "抽屉不存在")
    return success_response(drawer)


@app.put("/api/drawer/{drawer_id}", response_model=schemas.ResponseModel[schemas.Drawer])
def update_drawer(drawer_id: int, drawer: schemas.DrawerUpdate, db: Session = Depends(get_db)):
    db_drawer = db.query(Drawer).filter(Drawer.id == drawer_id).first()
    if not db_drawer:
        return error_response(404, "抽屉不存在")
    if drawer.location:
        existing = db.query(Drawer).filter(Drawer.location == drawer.location, Drawer.id != drawer_id).first()
        if existing:
            return error_response(400, "抽屉位置已存在")
    for key, value in drawer.model_dump(exclude_unset=True).items():
        setattr(db_drawer, key, value)
    db.commit()
    db.refresh(db_drawer)
    return success_response(db_drawer)


@app.delete("/api/drawer/{drawer_id}", response_model=schemas.ResponseModel)
def delete_drawer(drawer_id: int, db: Session = Depends(get_db)):
    db_drawer = db.query(Drawer).filter(Drawer.id == drawer_id).first()
    if not db_drawer:
        return error_response(404, "抽屉不存在")
    db.delete(db_drawer)
    db.commit()
    return success_response(None, "删除成功")


@app.post("/api/course-batch", response_model=schemas.ResponseModel[schemas.CourseBatch])
def create_course_batch(course: schemas.CourseBatchCreate, db: Session = Depends(get_db)):
    existing = db.query(CourseBatch).filter(CourseBatch.name == course.name).first()
    if existing:
        return error_response(400, "课程批次名称已存在")
    db_course = CourseBatch(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return success_response(db_course)


@app.get("/api/course-batch", response_model=schemas.ResponseModel[List[schemas.CourseBatch]])
def list_course_batch(db: Session = Depends(get_db)):
    courses = db.query(CourseBatch).all()
    return success_response(courses)


@app.get("/api/course-batch/{course_id}", response_model=schemas.ResponseModel[schemas.CourseBatch])
def get_course_batch(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseBatch).filter(CourseBatch.id == course_id).first()
    if not course:
        return error_response(404, "课程批次不存在")
    return success_response(course)


@app.put("/api/course-batch/{course_id}", response_model=schemas.ResponseModel[schemas.CourseBatch])
def update_course_batch(course_id: int, course: schemas.CourseBatchUpdate, db: Session = Depends(get_db)):
    db_course = db.query(CourseBatch).filter(CourseBatch.id == course_id).first()
    if not db_course:
        return error_response(404, "课程批次不存在")
    if course.name:
        existing = db.query(CourseBatch).filter(CourseBatch.name == course.name, CourseBatch.id != course_id).first()
        if existing:
            return error_response(400, "课程批次名称已存在")
    for key, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return success_response(db_course)


@app.delete("/api/course-batch/{course_id}", response_model=schemas.ResponseModel)
def delete_course_batch(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(CourseBatch).filter(CourseBatch.id == course_id).first()
    if not db_course:
        return error_response(404, "课程批次不存在")
    db.delete(db_course)
    db.commit()
    return success_response(None, "删除成功")


@app.post("/api/borrower", response_model=schemas.ResponseModel[schemas.Borrower])
def create_borrower(borrower: schemas.BorrowerCreate, db: Session = Depends(get_db)):
    if borrower.student_id:
        existing = db.query(Borrower).filter(Borrower.student_id == borrower.student_id).first()
        if existing:
            return error_response(400, "学号/工号已存在")
    db_borrower = Borrower(**borrower.model_dump())
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return success_response(db_borrower)


@app.get("/api/borrower", response_model=schemas.ResponseModel[List[schemas.Borrower]])
def list_borrower(db: Session = Depends(get_db)):
    borrowers = db.query(Borrower).all()
    return success_response(borrowers)


@app.get("/api/borrower/{borrower_id}", response_model=schemas.ResponseModel[schemas.Borrower])
def get_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if not borrower:
        return error_response(404, "借阅人不存在")
    return success_response(borrower)


@app.put("/api/borrower/{borrower_id}", response_model=schemas.ResponseModel[schemas.Borrower])
def update_borrower(borrower_id: int, borrower: schemas.BorrowerUpdate, db: Session = Depends(get_db)):
    db_borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if not db_borrower:
        return error_response(404, "借阅人不存在")
    if borrower.student_id:
        existing = db.query(Borrower).filter(Borrower.student_id == borrower.student_id, Borrower.id != borrower_id).first()
        if existing:
            return error_response(400, "学号/工号已存在")
    for key, value in borrower.model_dump(exclude_unset=True).items():
        setattr(db_borrower, key, value)
    db.commit()
    db.refresh(db_borrower)
    return success_response(db_borrower)


@app.delete("/api/borrower/{borrower_id}", response_model=schemas.ResponseModel)
def delete_borrower(borrower_id: int, db: Session = Depends(get_db)):
    db_borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if not db_borrower:
        return error_response(404, "借阅人不存在")
    db.delete(db_borrower)
    db.commit()
    return success_response(None, "删除成功")


@app.post("/api/thin-section", response_model=schemas.ResponseModel[schemas.ThinSection])
def create_thin_section(section: schemas.ThinSectionCreate, db: Session = Depends(get_db)):
    existing = db.query(ThinSection).filter(ThinSection.section_no == section.section_no).first()
    if existing:
        return error_response(400, "薄片编号已存在")
    if section.lithology_id:
        lithology = db.query(Lithology).filter(Lithology.id == section.lithology_id).first()
        if not lithology:
            return error_response(404, "岩性不存在")
    if section.drawer_id:
        drawer = db.query(Drawer).filter(Drawer.id == section.drawer_id).first()
        if not drawer:
            return error_response(404, "抽屉不存在")
    db_section = ThinSection(**section.model_dump())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return success_response(db_section)


@app.get("/api/thin-section", response_model=schemas.ResponseModel[List[schemas.ThinSection]])
def list_thin_section(db: Session = Depends(get_db)):
    sections = db.query(ThinSection).all()
    return success_response(sections)


@app.get("/api/thin-section/{section_id}", response_model=schemas.ResponseModel[schemas.ThinSection])
def get_thin_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    current_maintenance = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.thin_section_id == section_id,
        MaintenanceRecord.status == "维修中"
    ).first()
    section.current_maintenance = current_maintenance
    return success_response(section)


@app.put("/api/thin-section/{section_id}", response_model=schemas.ResponseModel[schemas.ThinSection])
def update_thin_section(section_id: int, section: schemas.ThinSectionUpdate, db: Session = Depends(get_db)):
    db_section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not db_section:
        return error_response(404, "薄片不存在")
    if section.section_no:
        existing = db.query(ThinSection).filter(ThinSection.section_no == section.section_no, ThinSection.id != section_id).first()
        if existing:
            return error_response(400, "薄片编号已存在")
    if section.lithology_id:
        lithology = db.query(Lithology).filter(Lithology.id == section.lithology_id).first()
        if not lithology:
            return error_response(404, "岩性不存在")
    if section.drawer_id:
        drawer = db.query(Drawer).filter(Drawer.id == section.drawer_id).first()
        if not drawer:
            return error_response(404, "抽屉不存在")
    for key, value in section.model_dump(exclude_unset=True).items():
        setattr(db_section, key, value)
    db.commit()
    db.refresh(db_section)
    return success_response(db_section)


@app.delete("/api/thin-section/{section_id}", response_model=schemas.ResponseModel)
def delete_thin_section(section_id: int, db: Session = Depends(get_db)):
    db_section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not db_section:
        return error_response(404, "薄片不存在")
    db.delete(db_section)
    db.commit()
    return success_response(None, "删除成功")


@app.post("/api/borrow", response_model=schemas.ResponseModel[schemas.BorrowRecord])
def create_borrow(record: schemas.BorrowRecordCreate, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == record.thin_section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    if section.status == "借出":
        return error_response(400, "该薄片已借出，不可重复借用")
    if section.status == "维修中":
        return error_response(400, "该薄片正在维修中，不可借出")
    if section.status == "报废":
        return error_response(400, "该薄片已报废，不可借出")
    if record.borrow_quantity <= 0:
        return error_response(400, "借出数量必须大于0")
    borrower = db.query(Borrower).filter(Borrower.id == record.borrower_id).first()
    if not borrower:
        return error_response(404, "借阅人不存在")
    if record.course_batch_id:
        course = db.query(CourseBatch).filter(CourseBatch.id == record.course_batch_id).first()
        if not course:
            return error_response(404, "课程批次不存在")
    
    db_record = BorrowRecord(**record.model_dump())
    db.add(db_record)
    section.status = "借出"
    db.commit()
    db.refresh(db_record)
    return success_response(db_record)


@app.put("/api/borrow/{record_id}/return", response_model=schemas.ResponseModel[schemas.BorrowRecord])
def return_borrow(record_id: int, return_data: schemas.BorrowRecordReturn, db: Session = Depends(get_db)):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        return error_response(404, "借阅记录不存在")
    if record.is_returned:
        return error_response(400, "该记录已归还")
    
    record.is_returned = True
    record.return_date = return_data.return_date
    record.has_crack = return_data.has_crack
    record.has_stain = return_data.has_stain
    record.label_worn = return_data.label_worn
    record.reinspection_result = return_data.reinspection_result
    record.return_remarks = return_data.return_remarks
    
    section = db.query(ThinSection).filter(ThinSection.id == record.thin_section_id).first()
    if section:
        section.status = "在库"
        if return_data.label_worn and section.label_status == "完好":
            section.label_status = "磨损"
        has_damage = return_data.has_crack or return_data.has_stain or return_data.label_worn
        if has_damage and return_data.reinspection_result != "合格":
            section.status = "维修中"
            damage_types = []
            if return_data.has_crack:
                damage_types.append("裂纹")
            if return_data.has_stain:
                damage_types.append("污渍")
            if return_data.label_worn:
                damage_types.append("标签磨损")
            damage_type = damage_types[0] if len(damage_types) == 1 else "其他"
            maintenance_record = MaintenanceRecord(
                thin_section_id=record.thin_section_id,
                borrow_record_id=record.id,
                problem_source="归还复检",
                damage_type=damage_type,
                damage_description=f"归还复检不合格：{'、'.join(damage_types)}",
                maintenance_person="待分配",
                send_date=return_data.return_date,
                status="维修中"
            )
            db.add(maintenance_record)
    
    db.commit()
    db.refresh(record)
    return success_response(record)


@app.get("/api/borrow", response_model=schemas.ResponseModel[List[schemas.BorrowRecord]])
def list_borrow(db: Session = Depends(get_db)):
    records = db.query(BorrowRecord).all()
    return success_response(records)


@app.get("/api/borrow/{record_id}", response_model=schemas.ResponseModel[schemas.BorrowRecord])
def get_borrow(record_id: int, db: Session = Depends(get_db)):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        return error_response(404, "借阅记录不存在")
    return success_response(record)


@app.get("/api/queue/overdue", response_model=schemas.ResponseModel[List[schemas.OverdueItem]])
def get_overdue_queue(db: Session = Depends(get_db)):
    today = date.today()
    records = db.query(BorrowRecord).filter(
        BorrowRecord.is_returned == False,
        BorrowRecord.expected_return_date < today
    ).all()
    
    result = []
    for record in records:
        overdue_days = (today - record.expected_return_date).days
        result.append({
            "borrow_id": record.id,
            "section_no": record.thin_section.section_no,
            "section_name": record.thin_section.name,
            "borrower_name": record.borrower.name,
            "expected_return_date": record.expected_return_date,
            "overdue_days": overdue_days
        })
    return success_response(result)


@app.get("/api/queue/damage-reinspection", response_model=schemas.ResponseModel[List[schemas.DamageReinspectionItem]])
def get_damage_reinspection_queue(db: Session = Depends(get_db)):
    records = db.query(BorrowRecord).filter(
        BorrowRecord.is_returned == True,
        or_(
            BorrowRecord.has_crack == True,
            BorrowRecord.has_stain == True,
            BorrowRecord.label_worn == True
        ),
        BorrowRecord.reinspection_result != "合格"
    ).all()
    
    result = []
    for record in records:
        damage_types = []
        if record.has_crack:
            damage_types.append("裂纹")
        if record.has_stain:
            damage_types.append("污渍")
        if record.label_worn:
            damage_types.append("标签磨损")
        maintenance = db.query(MaintenanceRecord).filter(
            MaintenanceRecord.borrow_record_id == record.id
        ).first()
        result.append({
            "borrow_id": record.id,
            "section_no": record.thin_section.section_no,
            "section_name": record.thin_section.name,
            "borrower_name": record.borrower.name,
            "damage_type": "、".join(damage_types),
            "return_date": record.return_date,
            "maintenance_status": maintenance.status if maintenance else None,
            "maintenance_id": maintenance.id if maintenance else None
        })
    return success_response(result)


@app.get("/api/queue/missing-label", response_model=schemas.ResponseModel[List[schemas.MissingLabelItem]])
def get_missing_label_queue(db: Session = Depends(get_db)):
    sections = db.query(ThinSection).filter(
        or_(
            ThinSection.label_status == "缺失",
            ThinSection.label_status == "磨损"
        )
    ).all()
    
    result = []
    for section in sections:
        last_borrow = db.query(BorrowRecord).filter(
            BorrowRecord.thin_section_id == section.id
        ).order_by(BorrowRecord.borrow_date.desc()).first()
        
        result.append({
            "section_id": section.id,
            "section_no": section.section_no,
            "section_name": section.name,
            "label_status": section.label_status,
            "last_borrow_date": last_borrow.borrow_date if last_borrow else None
        })
    return success_response(result)


@app.get("/api/search/thin-section", response_model=schemas.ResponseModel[List[schemas.ThinSection]])
def search_thin_section(
    lithology_id: Optional[int] = Query(None, description="岩性ID"),
    course_batch_id: Optional[int] = Query(None, description="课程批次ID"),
    section_no: Optional[str] = Query(None, description="薄片编号"),
    status: Optional[str] = Query(None, description="状态"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    db: Session = Depends(get_db)
):
    query = db.query(ThinSection)
    
    if lithology_id:
        query = query.filter(ThinSection.lithology_id == lithology_id)
    if section_no:
        query = query.filter(ThinSection.section_no.contains(section_no))
    if status:
        query = query.filter(ThinSection.status == status)
    
    if course_batch_id or start_date or end_date:
        query = query.join(BorrowRecord, ThinSection.id == BorrowRecord.thin_section_id)
        if course_batch_id:
            query = query.filter(BorrowRecord.course_batch_id == course_batch_id)
        if start_date:
            query = query.filter(BorrowRecord.borrow_date >= start_date)
        if end_date:
            query = query.filter(BorrowRecord.borrow_date <= end_date)
    
    sections = query.all()
    return success_response(sections)


@app.get("/api/statistics/damage-courses", response_model=schemas.ResponseModel[List[schemas.DamageCourseItem]])
def get_damage_courses(db: Session = Depends(get_db)):
    results = db.query(
        CourseBatch.id,
        CourseBatch.name,
        func.count(BorrowRecord.id).label("total_count"),
        func.sum(
            or_(
                BorrowRecord.has_crack == True,
                BorrowRecord.has_stain == True
            ).cast(Integer)
        ).label("damage_count")
    ).join(
        BorrowRecord, CourseBatch.id == BorrowRecord.course_batch_id, isouter=True
    ).group_by(CourseBatch.id).all()
    
    data = []
    for row in results:
        total = row.total_count or 0
        damage = row.damage_count or 0
        rate = (damage / total * 100) if total > 0 else 0
        data.append({
            "course_batch_id": row.id,
            "course_batch_name": row.name,
            "total_borrow_count": total,
            "damage_count": damage,
            "damage_rate": round(rate, 2)
        })
    
    data.sort(key=lambda x: x["damage_rate"], reverse=True)
    return success_response(data)


@app.get("/api/statistics/drawer-usage", response_model=schemas.ResponseModel[List[schemas.DrawerUsageItem]])
def get_drawer_usage(db: Session = Depends(get_db)):
    results = db.query(
        Drawer.id,
        Drawer.location,
        Drawer.capacity,
        func.count(ThinSection.id).label("used_count")
    ).join(
        ThinSection, Drawer.id == ThinSection.drawer_id, isouter=True
    ).group_by(Drawer.id).all()
    
    data = []
    for row in results:
        capacity = row.capacity or 50
        used = row.used_count or 0
        rate = (used / capacity * 100) if capacity > 0 else 0
        data.append({
            "drawer_id": row.id,
            "location": row.location,
            "capacity": capacity,
            "used_count": used,
            "usage_rate": round(rate, 2)
        })
    return success_response(data)


@app.get("/api/statistics/overdue-list", response_model=schemas.ResponseModel[List[schemas.OverdueItem]])
def get_overdue_list(db: Session = Depends(get_db)):
    today = date.today()
    records = db.query(BorrowRecord).filter(
        BorrowRecord.is_returned == False,
        BorrowRecord.expected_return_date < today
    ).order_by(BorrowRecord.expected_return_date.asc()).all()
    
    result = []
    for record in records:
        overdue_days = (today - record.expected_return_date).days
        result.append({
            "borrow_id": record.id,
            "section_no": record.thin_section.section_no,
            "section_name": record.thin_section.name,
            "borrower_name": record.borrower.name,
            "expected_return_date": record.expected_return_date,
            "overdue_days": overdue_days
        })
    return success_response(result)


def check_reservation_conflict(thin_section_id: int, db: Session, exclude_reservation_id: Optional[int] = None) -> Optional[str]:
    section = db.query(ThinSection).filter(ThinSection.id == thin_section_id).first()
    if section and section.status == "借出":
        return "该薄片已借出，不可预约"
    if section and section.status == "维修中":
        return "该薄片正在维修中，不可预约"
    if section and section.status == "报废":
        return "该薄片已报废，不可预约"
    
    query = db.query(BorrowReservation).filter(
        BorrowReservation.thin_section_id == thin_section_id,
        BorrowReservation.status.in_(["待审批", "已通过"])
    )
    if exclude_reservation_id:
        query = query.filter(BorrowReservation.id != exclude_reservation_id)
    existing = query.first()
    if existing:
        return "该薄片存在待审批或已通过的预约，不可重复预约"
    
    return None


@app.post("/api/reservation", response_model=schemas.ResponseModel[schemas.BorrowReservation])
def create_reservation(reservation: schemas.BorrowReservationCreate, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == reservation.thin_section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    
    conflict = check_reservation_conflict(reservation.thin_section_id, db)
    if conflict:
        return error_response(400, conflict)
    
    borrower = db.query(Borrower).filter(Borrower.id == reservation.borrower_id).first()
    if not borrower:
        return error_response(404, "借阅人不存在")
    
    if reservation.course_batch_id:
        course = db.query(CourseBatch).filter(CourseBatch.id == reservation.course_batch_id).first()
        if not course:
            return error_response(404, "课程批次不存在")
    
    db_reservation = BorrowReservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return success_response(db_reservation)


@app.get("/api/reservation", response_model=schemas.ResponseModel[List[schemas.BorrowReservation]])
def list_reservation(
    status: Optional[str] = Query(None, description="预约状态"),
    section_no: Optional[str] = Query(None, description="薄片编号"),
    borrower_name: Optional[str] = Query(None, description="借阅人姓名"),
    course_batch_id: Optional[int] = Query(None, description="课程批次ID"),
    start_date: Optional[date] = Query(None, description="预约开始日期"),
    end_date: Optional[date] = Query(None, description="预约结束日期"),
    db: Session = Depends(get_db)
):
    query = db.query(BorrowReservation)
    
    if status:
        query = query.filter(BorrowReservation.status == status)
    if course_batch_id:
        query = query.filter(BorrowReservation.course_batch_id == course_batch_id)
    if start_date:
        query = query.filter(BorrowReservation.reservation_date >= start_date)
    if end_date:
        query = query.filter(BorrowReservation.reservation_date <= end_date)
    
    if section_no or borrower_name:
        query = query.join(ThinSection, BorrowReservation.thin_section_id == ThinSection.id)
        query = query.join(Borrower, BorrowReservation.borrower_id == Borrower.id)
        if section_no:
            query = query.filter(ThinSection.section_no.contains(section_no))
        if borrower_name:
            query = query.filter(Borrower.name.contains(borrower_name))
    
    reservations = query.order_by(BorrowReservation.created_at.desc()).all()
    return success_response(reservations)


@app.get("/api/reservation/{reservation_id}", response_model=schemas.ResponseModel[schemas.BorrowReservation])
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(BorrowReservation).filter(BorrowReservation.id == reservation_id).first()
    if not reservation:
        return error_response(404, "预约记录不存在")
    return success_response(reservation)


@app.put("/api/reservation/{reservation_id}/approve", response_model=schemas.ResponseModel[schemas.BorrowReservation])
def approve_reservation(reservation_id: int, data: schemas.BorrowReservationApprove, db: Session = Depends(get_db)):
    reservation = db.query(BorrowReservation).filter(BorrowReservation.id == reservation_id).first()
    if not reservation:
        return error_response(404, "预约记录不存在")
    if reservation.status != "待审批":
        return error_response(400, "只有待审批状态的预约可以审批")
    
    conflict = check_reservation_conflict(reservation.thin_section_id, db, exclude_reservation_id=reservation_id)
    if conflict:
        return error_response(400, conflict)
    
    reservation.status = "已通过"
    reservation.approval_remarks = data.approval_remarks
    reservation.approved_by = data.approved_by
    reservation.approved_at = datetime.now()
    
    db.commit()
    db.refresh(reservation)
    return success_response(reservation)


@app.put("/api/reservation/{reservation_id}/reject", response_model=schemas.ResponseModel[schemas.BorrowReservation])
def reject_reservation(reservation_id: int, data: schemas.BorrowReservationReject, db: Session = Depends(get_db)):
    reservation = db.query(BorrowReservation).filter(BorrowReservation.id == reservation_id).first()
    if not reservation:
        return error_response(404, "预约记录不存在")
    if reservation.status != "待审批":
        return error_response(400, "只有待审批状态的预约可以拒绝")
    
    reservation.status = "已拒绝"
    reservation.approval_remarks = data.approval_remarks
    reservation.approved_by = data.approved_by
    reservation.approved_at = datetime.now()
    
    db.commit()
    db.refresh(reservation)
    return success_response(reservation)


@app.put("/api/reservation/{reservation_id}/cancel", response_model=schemas.ResponseModel[schemas.BorrowReservation])
def cancel_reservation(reservation_id: int, data: schemas.BorrowReservationCancel, db: Session = Depends(get_db)):
    reservation = db.query(BorrowReservation).filter(BorrowReservation.id == reservation_id).first()
    if not reservation:
        return error_response(404, "预约记录不存在")
    if reservation.status not in ["待审批", "已通过"]:
        return error_response(400, "只有待审批或已通过状态的预约可以取消")
    
    reservation.status = "已取消"
    if data.approval_remarks:
        reservation.approval_remarks = data.approval_remarks
    
    db.commit()
    db.refresh(reservation)
    return success_response(reservation)


@app.post("/api/reservation/{reservation_id}/convert", response_model=schemas.ResponseModel[schemas.BorrowRecord])
def convert_to_borrow(reservation_id: int, data: schemas.BorrowReservationConvert, db: Session = Depends(get_db)):
    reservation = db.query(BorrowReservation).filter(BorrowReservation.id == reservation_id).first()
    if not reservation:
        return error_response(404, "预约记录不存在")
    if reservation.status != "已通过":
        return error_response(400, "只有已通过状态的预约可以转正式借阅")
    
    section = db.query(ThinSection).filter(ThinSection.id == reservation.thin_section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    if section.status == "借出":
        return error_response(400, "该薄片已借出，不可重复借用")
    if section.status == "维修中":
        return error_response(400, "该薄片正在维修中，不可借出")
    if section.status == "报废":
        return error_response(400, "该薄片已报废，不可借出")

    borrow_record = BorrowRecord(
        thin_section_id=reservation.thin_section_id,
        borrower_id=reservation.borrower_id,
        course_batch_id=reservation.course_batch_id,
        purpose=reservation.purpose,
        borrow_quantity=data.borrow_quantity,
        appearance_grade=data.appearance_grade,
        expected_return_date=reservation.expected_return_date,
        borrow_date=data.borrow_date,
        remarks=reservation.remarks
    )
    
    db.add(borrow_record)
    section.status = "借出"
    reservation.status = "已转借出"
    
    db.commit()
    db.refresh(borrow_record)
    db.refresh(reservation)
    
    return success_response(borrow_record)


@app.post("/api/maintenance", response_model=schemas.ResponseModel[schemas.MaintenanceRecord])
def create_maintenance(record: schemas.MaintenanceRecordCreate, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == record.thin_section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    if section.status == "借出":
        return error_response(400, "该薄片已借出，不可创建维修记录")
    if section.status == "报废":
        return error_response(400, "该薄片已报废，不可创建维修记录")
    if section.status == "维修中":
        active_maintenance = db.query(MaintenanceRecord).filter(
            MaintenanceRecord.thin_section_id == record.thin_section_id,
            MaintenanceRecord.status == "维修中"
        ).first()
        if active_maintenance:
            return error_response(400, "该薄片已有进行中的维修记录")
    if record.borrow_record_id:
        borrow_record = db.query(BorrowRecord).filter(BorrowRecord.id == record.borrow_record_id).first()
        if not borrow_record:
            return error_response(404, "关联借阅记录不存在")
        if borrow_record.thin_section_id != record.thin_section_id:
            return error_response(400, "关联借阅记录与薄片不一致")
    if record.problem_source not in ["归还复检", "人工标记", "其他"]:
        return error_response(400, "问题来源必须为：归还复检/人工标记/其他")
    if record.damage_type not in ["裂纹", "污渍", "标签磨损", "破碎", "其他"]:
        return error_response(400, "损坏类型必须为：裂纹/污渍/标签磨损/破碎/其他")

    db_record = MaintenanceRecord(**record.model_dump())
    db.add(db_record)
    section.status = "维修中"
    db.commit()
    db.refresh(db_record)
    return success_response(db_record)


@app.get("/api/maintenance", response_model=schemas.ResponseModel[List[schemas.MaintenanceRecordItem]])
def list_maintenance(
    status: Optional[str] = Query(None, description="维修状态：维修中/已完成"),
    damage_type: Optional[str] = Query(None, description="损坏类型"),
    problem_source: Optional[str] = Query(None, description="问题来源"),
    maintenance_person: Optional[str] = Query(None, description="维修负责人"),
    section_no: Optional[str] = Query(None, description="薄片编号"),
    start_date: Optional[date] = Query(None, description="送修开始日期"),
    end_date: Optional[date] = Query(None, description="送修结束日期"),
    result: Optional[str] = Query(None, description="维修结果"),
    db: Session = Depends(get_db)
):
    query = db.query(MaintenanceRecord)

    if status:
        query = query.filter(MaintenanceRecord.status == status)
    if damage_type:
        query = query.filter(MaintenanceRecord.damage_type == damage_type)
    if problem_source:
        query = query.filter(MaintenanceRecord.problem_source == problem_source)
    if maintenance_person:
        query = query.filter(MaintenanceRecord.maintenance_person.contains(maintenance_person))
    if start_date:
        query = query.filter(MaintenanceRecord.send_date >= start_date)
    if end_date:
        query = query.filter(MaintenanceRecord.send_date <= end_date)
    if result:
        query = query.filter(MaintenanceRecord.result == result)

    if section_no:
        query = query.join(ThinSection, MaintenanceRecord.thin_section_id == ThinSection.id)
        query = query.filter(ThinSection.section_no.contains(section_no))

    records = query.order_by(MaintenanceRecord.created_at.desc()).all()

    result_list = []
    for record in records:
        section = db.query(ThinSection).filter(ThinSection.id == record.thin_section_id).first()
        result_list.append({
            "id": record.id,
            "thin_section_id": record.thin_section_id,
            "section_no": section.section_no if section else None,
            "section_name": section.name if section else None,
            "problem_source": record.problem_source,
            "damage_type": record.damage_type,
            "damage_description": record.damage_description,
            "maintenance_person": record.maintenance_person,
            "send_date": record.send_date,
            "expected_completion_date": record.expected_completion_date,
            "actual_completion_date": record.actual_completion_date,
            "result": record.result,
            "processing_notes": record.processing_notes,
            "status": record.status
        })
    return success_response(result_list)


@app.get("/api/maintenance/{record_id}", response_model=schemas.ResponseModel[schemas.MaintenanceRecord])
def get_maintenance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()
    if not record:
        return error_response(404, "维修记录不存在")
    return success_response(record)


@app.put("/api/maintenance/{record_id}/complete", response_model=schemas.ResponseModel[schemas.MaintenanceRecord])
def complete_maintenance(record_id: int, data: schemas.MaintenanceRecordComplete, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()
    if not record:
        return error_response(404, "维修记录不存在")
    if record.status == "已完成":
        return error_response(400, "该维修记录已处理完成")
    if data.result not in ["维修完成", "报废", "恢复在库"]:
        return error_response(400, "维修结果必须为：维修完成/报废/恢复在库")

    record.status = "已完成"
    record.result = data.result
    record.processing_notes = data.processing_notes
    record.actual_completion_date = data.actual_completion_date or date.today()

    section = db.query(ThinSection).filter(ThinSection.id == record.thin_section_id).first()
    if section:
        if data.result == "维修完成":
            section.status = "在库"
            if record.damage_type == "标签磨损" and section.label_status in ["磨损", "缺失"]:
                section.label_status = "完好"
            section.remarks = (section.remarks or "") + f"；{date.today()}维修完成：{data.processing_notes or '无说明'}"
        elif data.result == "报废":
            section.status = "报废"
            section.remarks = (section.remarks or "") + f"；{date.today()}报废：{data.processing_notes or '无说明'}"
        elif data.result == "恢复在库":
            section.status = "在库"
            section.remarks = (section.remarks or "") + f"；{date.today()}恢复在库：{data.processing_notes or '无说明'}"

        other_active = db.query(MaintenanceRecord).filter(
            MaintenanceRecord.thin_section_id == record.thin_section_id,
            MaintenanceRecord.id != record_id,
            MaintenanceRecord.status == "维修中"
        ).first()
        if not other_active and section.status == "维修中":
            section.status = "在库"

    db.commit()
    db.refresh(record)
    return success_response(record)


@app.get("/api/maintenance/thin-section/{section_id}", response_model=schemas.ResponseModel[List[schemas.MaintenanceRecord]])
def get_thin_section_maintenance_history(section_id: int, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    records = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.thin_section_id == section_id
    ).order_by(MaintenanceRecord.created_at.desc()).all()
    return success_response(records)


@app.get("/api/statistics/maintenance", response_model=schemas.ResponseModel[schemas.MaintenanceStatisticsItem])
def get_maintenance_statistics(db: Session = Depends(get_db)):
    total = db.query(func.count(MaintenanceRecord.id)).scalar() or 0
    in_progress = db.query(func.count(MaintenanceRecord.id)).filter(
        MaintenanceRecord.status == "维修中"
    ).scalar() or 0
    completed = db.query(func.count(MaintenanceRecord.id)).filter(
        MaintenanceRecord.status == "已完成",
        MaintenanceRecord.result == "维修完成"
    ).scalar() or 0
    scrapped = db.query(func.count(MaintenanceRecord.id)).filter(
        MaintenanceRecord.status == "已完成",
        MaintenanceRecord.result == "报废"
    ).scalar() or 0
    restored = db.query(func.count(MaintenanceRecord.id)).filter(
        MaintenanceRecord.status == "已完成",
        MaintenanceRecord.result == "恢复在库"
    ).scalar() or 0

    return success_response({
        "total_count": total,
        "in_progress_count": in_progress,
        "completed_count": completed,
        "scrapped_count": scrapped,
        "restored_count": restored
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8066)
