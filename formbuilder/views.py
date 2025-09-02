import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
        form = FormSchema.objects.create(
            name=payload.get("name", "Untitled Form"),
            description=payload.get("description", ""),
            fields=payload.get("fields", []),
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
        form_schema.name = payload.get("name", form_schema.name)
        form_schema.description = payload.get("description", form_schema.description)
        form_schema.fields = payload.get("fields", [])
        form_schema.save()
        return JsonResponse({"ok": True})

    # ✅ Pass safe JSON-ready dict to template
    schema_dict = {
        "id": form_schema.id,
        "name": form_schema.name,
        "description": form_schema.description,
        "fields": json.dumps(form_schema.fields),  # ensure JSON string
    }
    return render(request, "formbuilder/editor.html", {"form_schema": schema_dict})


@login_required
def form_delete(request, pk):
    """Delete a form schema."""
    form_schema = get_object_or_404(FormSchema, pk=pk, owner=request.user)
    form_schema.delete()
    return redirect("form_list")