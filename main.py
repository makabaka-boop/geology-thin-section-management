from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, Integer
from datetime import date, datetime
from typing import Optional, List

from database import engine, get_db, Base
from models import Lithology, Drawer, CourseBatch, Borrower, ThinSection, BorrowRecord, BorrowReservation, RepairRecord
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


@app.get("/api/thin-section/{section_id}", response_model=schemas.ResponseModel[schemas.ThinSectionDetail])
def get_thin_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not section:
        return error_response(404, "薄片不存在")

    repair_records = db.query(RepairRecord).filter(
        RepairRecord.thin_section_id == section_id
    ).order_by(RepairRecord.created_at.desc()).all()

    section.repair_records = repair_records
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
    if section.status and section.status != db_section.status:
        if db_section.status == "维修中" and section.status != "维修中":
            return error_response(400, "维修中的薄片不可直接修改状态，请通过维修完成接口处理")
        if db_section.status == "借出" and section.status != "借出":
            return error_response(400, "借出中的薄片不可直接修改状态，请通过归还接口处理")
        if db_section.status == "报废" and section.status != "报废":
            return error_response(400, "已报废的薄片不可直接修改状态")
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
        if (return_data.has_crack or return_data.has_stain or return_data.label_worn) and return_data.reinspection_result != "合格":
            section.status = "维修中"

            damage_types = []
            if return_data.has_crack:
                damage_types.append("裂纹")
            if return_data.has_stain:
                damage_types.append("污渍")
            if return_data.label_worn:
                damage_types.append("标签磨损")
            damage_type_str = "、".join(damage_types) if damage_types else "其他"

            existing_repair = db.query(RepairRecord).filter(
                RepairRecord.thin_section_id == record.thin_section_id,
                RepairRecord.status == "维修中"
            ).first()
            if not existing_repair:
                repair_record = RepairRecord(
                    thin_section_id=record.thin_section_id,
                    problem_source="归还复检",
                    damage_type=damage_type_str,
                    send_date=return_data.return_date,
                    related_borrow_id=record.id,
                    handle_remark=return_data.return_remarks
                )
                db.add(repair_record)

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

        repair_record = db.query(RepairRecord).filter(
            RepairRecord.thin_section_id == record.thin_section_id,
            RepairRecord.related_borrow_id == record.id
        ).first()

        result.append({
            "borrow_id": record.id,
            "section_id": record.thin_section_id,
            "section_no": record.thin_section.section_no,
            "section_name": record.thin_section.name,
            "borrower_name": record.borrower.name,
            "damage_type": "、".join(damage_types) if damage_types else "其他",
            "return_date": record.return_date,
            "repair_status": repair_record.status if repair_record else None,
            "repair_id": repair_record.id if repair_record else None
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

        repair_record = db.query(RepairRecord).filter(
            RepairRecord.thin_section_id == section.id,
            RepairRecord.status == "维修中"
        ).first()

        result.append({
            "section_id": section.id,
            "section_no": section.section_no,
            "section_name": section.name,
            "label_status": section.label_status,
            "last_borrow_date": last_borrow.borrow_date if last_borrow else None,
            "repair_status": repair_record.status if repair_record else None,
            "repair_id": repair_record.id if repair_record else None
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
    if section:
        if section.status == "借出":
            return "该薄片已借出，不可预约"
        if section.status == "维修中":
            return "该薄片正在维修中，不可预约"
        if section.status == "报废":
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


@app.post("/api/repair", response_model=schemas.ResponseModel[schemas.RepairRecord])
def create_repair_record(repair: schemas.RepairRecordCreate, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == repair.thin_section_id).first()
    if not section:
        return error_response(404, "薄片不存在")
    if section.status == "借出":
        return error_response(400, "该薄片已借出，不可创建维修记录")
    if section.status == "报废":
        return error_response(400, "该薄片已报废，不可创建维修记录")

    existing_repair = db.query(RepairRecord).filter(
        RepairRecord.thin_section_id == repair.thin_section_id,
        RepairRecord.status == "维修中"
    ).first()
    if existing_repair:
        return error_response(400, "该薄片存在进行中的维修记录，不可重复创建")

    if repair.related_borrow_id:
        borrow = db.query(BorrowRecord).filter(BorrowRecord.id == repair.related_borrow_id).first()
        if not borrow:
            return error_response(404, "关联借阅记录不存在")

    db_repair = RepairRecord(**repair.model_dump())
    db.add(db_repair)
    section.status = "维修中"
    db.commit()
    db.refresh(db_repair)
    return success_response(db_repair)


@app.get("/api/repair", response_model=schemas.ResponseModel[schemas.PageResult[schemas.RepairRecord]])
def list_repair_records(
    status: Optional[str] = Query(None, description="维修状态"),
    section_no: Optional[str] = Query(None, description="薄片编号"),
    problem_source: Optional[str] = Query(None, description="问题来源"),
    damage_type: Optional[str] = Query(None, description="损坏类型"),
    repair_person: Optional[str] = Query(None, description="维修负责人"),
    start_date: Optional[date] = Query(None, description="送修开始日期"),
    end_date: Optional[date] = Query(None, description="送修结束日期"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
    db: Session = Depends(get_db)
):
    query = db.query(RepairRecord)

    if status:
        query = query.filter(RepairRecord.status == status)
    if problem_source:
        query = query.filter(RepairRecord.problem_source == problem_source)
    if damage_type:
        query = query.filter(RepairRecord.damage_type.contains(damage_type))
    if repair_person:
        query = query.filter(RepairRecord.repair_person.contains(repair_person))
    if start_date:
        query = query.filter(RepairRecord.send_date >= start_date)
    if end_date:
        query = query.filter(RepairRecord.send_date <= end_date)

    if section_no:
        query = query.join(ThinSection, RepairRecord.thin_section_id == ThinSection.id)
        query = query.filter(ThinSection.section_no.contains(section_no))

    total = query.count()
    records = query.order_by(RepairRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result = {
        "total": total,
        "items": records
    }
    return success_response(result)


@app.get("/api/repair/{repair_id}", response_model=schemas.ResponseModel[schemas.RepairRecord])
def get_repair_record(repair_id: int, db: Session = Depends(get_db)):
    repair = db.query(RepairRecord).filter(RepairRecord.id == repair_id).first()
    if not repair:
        return error_response(404, "维修记录不存在")
    return success_response(repair)


@app.put("/api/repair/{repair_id}", response_model=schemas.ResponseModel[schemas.RepairRecord])
def update_repair_record(repair_id: int, repair_data: schemas.RepairRecordUpdate, db: Session = Depends(get_db)):
    repair = db.query(RepairRecord).filter(RepairRecord.id == repair_id).first()
    if not repair:
        return error_response(404, "维修记录不存在")
    if repair.status != "维修中":
        return error_response(400, "只有维修中的记录可以修改")

    for key, value in repair_data.model_dump(exclude_unset=True).items():
        setattr(repair, key, value)

    db.commit()
    db.refresh(repair)
    return success_response(repair)


@app.put("/api/repair/{repair_id}/complete", response_model=schemas.ResponseModel[schemas.RepairRecord])
def complete_repair_record(repair_id: int, complete_data: schemas.RepairRecordComplete, db: Session = Depends(get_db)):
    repair = db.query(RepairRecord).filter(RepairRecord.id == repair_id).first()
    if not repair:
        return error_response(404, "维修记录不存在")
    if repair.status != "维修中":
        return error_response(400, "只有维修中的记录可以完成")

    valid_results = ["维修完成", "报废", "恢复在库"]
    if complete_data.repair_result not in valid_results:
        return error_response(400, f"维修结果必须是以下之一：{', '.join(valid_results)}")

    section = db.query(ThinSection).filter(ThinSection.id == repair.thin_section_id).first()
    if not section:
        return error_response(404, "关联薄片不存在")

    repair.status = "已完成"
    repair.repair_result = complete_data.repair_result
    repair.actual_complete_date = complete_data.actual_complete_date or date.today()
    if complete_data.handle_remark:
        repair.handle_remark = complete_data.handle_remark

    if complete_data.repair_result == "维修完成" or complete_data.repair_result == "恢复在库":
        section.status = "在库"
    elif complete_data.repair_result == "报废":
        section.status = "报废"

    if complete_data.update_label_status is not None:
        section.label_status = complete_data.update_label_status
    else:
        if complete_data.repair_result == "维修完成":
            if repair.damage_type and "标签" in repair.damage_type:
                section.label_status = "完好"
        elif complete_data.repair_result == "报废":
            section.label_status = "缺失"

    auto_remark = f"【{repair.repair_result}】{repair.actual_complete_date}，维修负责人：{repair.repair_person or '未指定'}"
    if complete_data.handle_remark:
        auto_remark += f"，处理说明：{complete_data.handle_remark}"

    if complete_data.update_remarks is not None:
        if section.remarks:
            section.remarks = section.remarks + "\n" + complete_data.update_remarks
        else:
            section.remarks = complete_data.update_remarks
    else:
        if section.remarks:
            section.remarks = section.remarks + "\n" + auto_remark
        else:
            section.remarks = auto_remark

    db.commit()
    db.refresh(repair)
    return success_response(repair)


@app.get("/api/repair/thin-section/{section_id}", response_model=schemas.ResponseModel[List[schemas.RepairRecord]])
def get_repair_history(section_id: int, db: Session = Depends(get_db)):
    section = db.query(ThinSection).filter(ThinSection.id == section_id).first()
    if not section:
        return error_response(404, "薄片不存在")

    records = db.query(RepairRecord).filter(
        RepairRecord.thin_section_id == section_id
    ).order_by(RepairRecord.created_at.desc()).all()

    return success_response(records)


@app.get("/api/statistics/repair-status", response_model=schemas.ResponseModel[List[schemas.RepairStatisticsItem]])
def get_repair_statistics(db: Session = Depends(get_db)):
    results = db.query(
        RepairRecord.status,
        func.count(RepairRecord.id).label("count")
    ).group_by(RepairRecord.status).all()

    data = []
    status_map = {
        "维修中": 0,
        "已完成": 0
    }
    for row in results:
        status_map[row.status] = row.count

    for status, count in status_map.items():
        data.append({
            "status": status,
            "count": count
        })

    return success_response(data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8066)
