from django.shortcuts import render, redirect, get_object_or_404
from .models import Secteur, Rue
from .forms import SecteurForm, RueForm
from core.decorators import agent_required, comptable_required, gestionnaire_required, admin_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# --- SECTEURS ---


@gestionnaire_required
@login_required
def liste_secteurs(request):
    # Récupérer tous les secteurs avec leurs rues
    secteurs_list = Secteur.objects.all().prefetch_related("rues").order_by("nom")

    # Pagination : 10 secteurs par page
    paginator = Paginator(secteurs_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_secteurs": secteurs_list.count(),
    }
    return render(request, "secteurs/liste.html", context)


@gestionnaire_required
@login_required
def create_secteur(request):
    if request.method == "POST":
        form = SecteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("secteurs:liste")
    else:
        form = SecteurForm(initial={"ville": "Brazzaville", "pays": "Congo"})
    return render(request, "secteurs/create.html", {"form": form})

@gestionnaire_required
@login_required
def edit_secteur(request, id):
    secteur = get_object_or_404(Secteur, id=id)
    if request.method == "POST":
        form = SecteurForm(request.POST, instance=secteur)
        if form.is_valid():
            form.save()
            return redirect("secteurs:liste")
    else:
        form = SecteurForm(instance=secteur)
    return render(request, "secteurs/edit.html", {"form": form, "secteur": secteur})


@gestionnaire_required
@login_required
def detail_secteur(request, id):
    secteur = get_object_or_404(Secteur, id=id)
    rues = secteur.rues.all()
    compteur_rues = rues.count()
    return render(request, "secteurs/detail.html", {
        "secteur": secteur,
        "rues": rues,
        "compteur_rues": compteur_rues
    })

@gestionnaire_required
@login_required
def delete_secteur(request, id):
    secteur = get_object_or_404(Secteur, id=id)
    secteur.delete()
    return redirect("secteurs:liste")


# --- RUES ---
@gestionnaire_required
@login_required
def liste_rues(request):
    # Récupérer toutes les rues avec leur secteur
    rues_list = Rue.objects.select_related("secteur").order_by("nom")

    # Pagination : 10 rues par page
    paginator = Paginator(rues_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_rues": rues_list.count(),
    }
    return render(request, "secteurs/liste_rues.html", context)


@gestionnaire_required
@login_required
def create_rue(request, secteur_id):
    secteur = get_object_or_404(Secteur, id=secteur_id)
    if request.method == "POST":
        form = RueForm(request.POST)
        if form.is_valid():
            rue = form.save(commit=False)
            rue.secteur = secteur
            rue.save()
            return redirect("secteurs:liste_rues")
    else:
        form = RueForm(initial={"secteur": secteur})
    return render(request, "secteurs/create_rue.html", {"form": form, "secteur": secteur})


@gestionnaire_required
@login_required
def edit_rue(request, id):
    rue = get_object_or_404(Rue, id=id)
    if request.method == "POST":
        form = RueForm(request.POST, instance=rue)
        if form.is_valid():
            form.save()
            return redirect("secteurs:liste_rues")
    else:
        form = RueForm(instance=rue)
    return render(request, "secteurs/edit_rue.html", {"form": form, "rue": rue})

@gestionnaire_required
@login_required
def delete_rue(request, id):
    rue = get_object_or_404(Rue, id=id)
    rue.delete()
    return redirect("secteurs:liste_rues")

@gestionnaire_required
@login_required
def create_rue_global(request):
    if request.method == "POST":
        form = RueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("secteurs:liste_rues")
    else:
        form = RueForm()
    return render(request, "secteurs/create_rue_global.html", {"form": form})

