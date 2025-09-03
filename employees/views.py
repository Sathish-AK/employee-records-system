from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployeeRecord
from django.http import JsonResponse
from formbuilder.models import FormSchema
import json
from django.db.models import Q

@login_required
def employee_delete(request, pk):
    rec = get_object_or_404(EmployeeRecord, pk=pk, created_by=request.user)
    rec.delete()
    messages.success(request, "Employee deleted")
    return redirect("employee_list")


@login_required
def employee_edit(request, pk):
    rec = get_object_or_404(EmployeeRecord, pk=pk, created_by=request.user)
    forms = FormSchema.objects.filter(owner=request.user)

    if request.method == "POST":
        payload = json.loads(request.body.decode())

        # ✅ Update form if changed
        form_id = payload.get("form_id")
        if form_id:
            rec.form_id = form_id

        # ✅ Update employee data
        rec.data = payload.get("data", rec.data)
        rec.save()

        return JsonResponse({"ok": True})

    form_data = [
        {"id": f.id, "name": f.name, "fields": f.fields}
        for f in forms
    ]
    return render(request, "employees/editor.html", {"record": rec, "forms": form_data})

@login_required
def employee_list(request):
    q = request.GET.get("q", "")
    records = EmployeeRecord.objects.filter(created_by=request.user).select_related("form")

    if q:
        if q.isdigit():
            # 🔎 If query is numeric, search by ID, form name, or data
            records = records.filter(
                Q(id=int(q)) |
                Q(data__icontains=q) |
                Q(form__name__icontains=q)   # ✅ added
            )
        else:
            # 🔎 Otherwise search in data and form name
            records = records.filter(
                Q(data__icontains=q) |
                Q(form__name__icontains=q)   # ✅ added
            )

    return render(request, "employees/list.html", {"records": records, "query": q})

@login_required
def employee_new(request):
    forms = FormSchema.objects.filter(owner=request.user)
    if request.method == "POST":
        payload = json.loads(request.body.decode())
        form_id = payload.get("form_id")
        form = get_object_or_404(FormSchema, id=form_id, owner=request.user)
        data = payload.get("data", {})

        # 🔒 Validate required fields
        missing = []
        for field in form.fields:
            if field.get("required") and not data.get(field["name"]):
                missing.append(field["label"])
        if missing:
            return JsonResponse(
                {"ok": False, "error": f"Missing required fields: {', '.join(missing)}"},
                status=400
            )

        rec = EmployeeRecord.objects.create(
            form=form, data=data, created_by=request.user
        )
        return JsonResponse({"id": rec.id, "ok": True})

    form_data = [{"id": f.id, "name": f.name, "fields": f.fields} for f in forms]
    return render(request, "employees/editor.html", {"forms": form_data})