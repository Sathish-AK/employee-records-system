import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import FormSchema


@login_required
def form_list(request):
    """List all forms created by the user."""
    forms = FormSchema.objects.filter(owner=request.user).order_by("-id")
    return render(request, "formbuilder/list.html", {"forms": forms})


@login_required
def form_new(request):
    """Create a new form schema."""
    if request.method == "POST":
        payload = json.loads(request.body.decode())

        # ✅ Require form name
        form_name = payload.get("name", "").strip()
        if not form_name:
            return HttpResponseBadRequest("⚠ Form name is required")

        # ✅ Check duplicate name for this user
        if FormSchema.objects.filter(owner=request.user, name=form_name).exists():
            return JsonResponse({"error": "⚠ A form with this name already exists"}, status=400)

        # ✅ At least one field
        fields = payload.get("fields", [])
        if not fields:
            return HttpResponseBadRequest("⚠ A form must contain at least one field")

        # ✅ Validate fields
        seen_names, seen_labels = set(), set()
        for f in fields:
            if not f.get("name") or not f.get("label") or not f.get("type"):
                return HttpResponseBadRequest("⚠ Each field must have a name, label, and type")
            if f["name"] in seen_names:
                return HttpResponseBadRequest(f"⚠ Duplicate field name: {f['name']}")
            if f["label"] in seen_labels:
                return HttpResponseBadRequest(f"⚠ Duplicate field label: {f['label']}")
            seen_names.add(f["name"])
            seen_labels.add(f["label"])

        form = FormSchema.objects.create(
            name=form_name,
            description=payload.get("description", ""),
            fields=fields,
            owner=request.user,
        )
        return JsonResponse({"id": form.id, "ok": True})

    schema_dict = {"id": None, "name": "", "description": "", "fields": []}
    return render(request, "formbuilder/editor.html", {"form_schema": schema_dict})


@login_required
def form_edit(request, pk):
    """Edit an existing form schema."""
    form_schema = get_object_or_404(FormSchema, pk=pk, owner=request.user)

    if request.method == "POST":
        payload = json.loads(request.body.decode())

        # ✅ Require form name
        form_name = payload.get("name", "").strip()
        if not form_name:
            return HttpResponseBadRequest("⚠ Form name is required")

        # ✅ Check duplicate name (exclude current one)
        existing = FormSchema.objects.filter(owner=request.user, name=form_name).exclude(pk=pk)
        if existing.exists():
            return JsonResponse({"error": "⚠ A form with this name already exists"}, status=400)

        # ✅ At least one field
        fields = payload.get("fields", [])
        if not fields:
            return HttpResponseBadRequest("⚠ A form must contain at least one field")

        # ✅ Validate fields
        seen_names, seen_labels = set(), set()
        for f in fields:
            if not f.get("name") or not f.get("label") or not f.get("type"):
                return HttpResponseBadRequest("⚠ Each field must have a name, label, and type")
            if f["name"] in seen_names:
                return HttpResponseBadRequest(f"⚠ Duplicate field name: {f['name']}")
            if f["label"] in seen_labels:
                return HttpResponseBadRequest(f"⚠ Duplicate field label: {f['label']}")
            seen_names.add(f["name"])
            seen_labels.add(f["label"])

        # ✅ Save
        form_schema.name = form_name
        form_schema.description = payload.get("description", "")
        form_schema.fields = fields
        form_schema.save()
        return JsonResponse({"ok": True})

    # Pass safe dict to template
    schema_dict = {
        "id": form_schema.id,
        "name": form_schema.name,
        "description": form_schema.description,
        "fields": json.dumps(form_schema.fields),  # JSON string for template
    }
    return render(request, "formbuilder/editor.html", {"form_schema": schema_dict})


@login_required
def form_delete(request, pk):
    """Delete a form schema."""
    form_schema = get_object_or_404(FormSchema, pk=pk, owner=request.user)
    form_schema.delete()
    return redirect("form_list")
