from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, Presentation
from .forms import GroupForm, PresentationForm

@login_required
def dashboard(request):
    groups = Group.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            g = form.save(commit=False)
            g.owner = request.user
            g.save()
            messages.success(request, "Группа создана.")
            return redirect('dashboard')
    else:
        form = GroupForm()
    return render(request, 'group_form.html', {'form': form})

@login_required
def edit_group(request, pk):
    group = get_object_or_404(Group, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Группа обновлена.")
            return redirect('dashboard')
    else:
        form = GroupForm(instance=group)
    return render(request, 'group_form.html', {'form': form, 'edit': True})

@login_required
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk, owner=request.user)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Группа удалена.")
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'object': group, 'type': 'group'})

@login_required
def upload_presentations(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, owner=request.user)
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            messages.error(request, "Не выбраны файлы.")
            return redirect('dashboard')
        for f in files:
            pres = Presentation(group=group, file=f, uploaded_by=request.user)
            pres.save()
        messages.success(request, "Файлы загружены.")
        return redirect('dashboard')
    return render(request, 'presentation_form.html', {'group': group})

@login_required
def delete_presentation(request, pk):
    pres = get_object_or_404(Presentation, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        pres.file.delete(save=False)
        pres.delete()
        messages.success(request, "Презентация удалена.")
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'object': pres, 'type': 'presentation'})
