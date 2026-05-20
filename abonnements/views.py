from django.shortcuts import render, redirect, get_object_or_404
from .models import Abonnement, TarifHistorique, OptionService
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from core.decorators import agent_required, comptable_required, gestionnaire_required, admin_required
from django.contrib import messages
from django.core.paginator import Paginator

# LISTE


@gestionnaire_required
@login_required
def liste_abonnements(request):
    abonnements_list = Abonnement.objects.all().order_by("nom")  # tri optionnel

    # Pagination : 10 abonnements par page
    paginator = Paginator(abonnements_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_abonnements": abonnements_list.count(),
    }
    return render(request, "abonnements/liste.html", context)



# CREATION
@gestionnaire_required
@login_required
def create_abonnement(request):
    if request.method == "POST":
        abonnement = Abonnement.objects.create(
            nom=request.POST["nom"],
            montant_base=request.POST["montant_base"],
            description=request.POST.get("description"),
            avantages=request.POST.get("avantages"),
        )
        
        # 🔒 AuditLog
        from accounts.models import AuditLog
        AuditLog.objects.create(
            utilisateur=request.user,
            action="Création",
            entite="Abonnement",
            entite_id=abonnement.id,
            details=f"Création de l'abonnement {abonnement.nom}"
        )
        
        return redirect("abonnements:liste")

    return render(request, "abonnements/create.html")


# MODIFICATION
@gestionnaire_required
@login_required
def edit_abonnement(request, id):
    abonnement = get_object_or_404(Abonnement, id=id)

    if request.method == "POST":
        ancien_montant = abonnement.montant_base

        abonnement.nom = request.POST["nom"]
        abonnement.montant_base = request.POST["montant_base"]
        abonnement.description = request.POST.get("description")
        abonnement.avantages = request.POST.get("avantages")
        abonnement.save()

        # Si le montant change → on crée un historique
        if Decimal(str(ancien_montant)) != Decimal(str(abonnement.montant_base)):
            TarifHistorique.objects.create(
                abonnement=abonnement,
                ancien_montant=ancien_montant,
                nouveau_montant=abonnement.montant_base,
                date_changement=timezone.now().date(),
                note="Modification du montant"
            )

        # 🔒 AuditLog
        from accounts.models import AuditLog
        AuditLog.objects.create(
            utilisateur=request.user,
            action="Modification",
            entite="Abonnement",
            entite_id=abonnement.id,
            details=f"Modification de l'abonnement {abonnement.nom}"
        )

        return redirect("abonnements:detail", abonnement.id)

    return render(request, "abonnements/edit.html", {"abonnement": abonnement})


# DETAILS
@gestionnaire_required
@login_required
def detail_abonnement(request, id):
    abonnement = get_object_or_404(Abonnement, id=id)
    options = abonnement.options.all()
    historique = abonnement.historique.all().order_by("-date_changement")

    return render(request, "abonnements/detail.html", {
        "abonnement": abonnement,
        "options": options,
        "historique": historique,
    })  

@gestionnaire_required
@login_required
def delete_abonnement(request, id):
    abonnement = get_object_or_404(Abonnement, id=id)

    if request.method == "POST":
        abonnement_id = abonnement.id
        abonnement_nom = abonnement.nom
        abonnement.delete()
        
        # 🔒 AuditLog
        from accounts.models import AuditLog
        AuditLog.objects.create(
            utilisateur=request.user,
            action="Suppression",
            entite="Abonnement",
            entite_id=abonnement_id,
            details=f"Suppression de l'abonnement {abonnement_nom}"
        )
        
        messages.success(request, "Abonnement supprimé avec succès.")
        return redirect("abonnements:liste")
    
    return redirect("abonnements:liste")

@gestionnaire_required
@login_required
def historique_tarifs(request):
    historique = TarifHistorique.objects.select_related("abonnement").order_by("-date_changement")
    return render(request, "abonnements/historique.html", {"historique": historique})


# LISTE GLOBALE

@gestionnaire_required
@login_required
def liste_options(request):
    # Récupérer toutes les options triées par nom
    options_list = OptionService.objects.all().order_by("nom")

    # Pagination : 10 options par page
    paginator = Paginator(options_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_options": options_list.count(),
    }
    return render(request, "options/liste.html", context)



# CREATION (LIÉE À UN ABONNEMENT)

from django.shortcuts import render, redirect
from .models import OptionService
from .forms import OptionServiceForm
@gestionnaire_required
@login_required
def create_option(request, abonnement_id):
    abonnement = get_object_or_404(Abonnement, id=abonnement_id)

    if request.method == "POST":
        form = OptionServiceForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.abonnement = abonnement
            option.save()
            return redirect("abonnements:detail", abonnement.id)
    else:
        form = OptionServiceForm()

    return render(request, "options/create1.html", {"form": form, "abonnement": abonnement})


@gestionnaire_required
@login_required
def create_option_global(request):
    if request.method == "POST":
        form = OptionServiceForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.abonnement = None  # option indépendante
            option.save()
            return redirect("abonnements:liste_options")
    else:
        form = OptionServiceForm()

    return render(request, "options/create1.html", {"form": form})


# MODIFICATION
@gestionnaire_required
@login_required
def edit_option(request, id):
    option = get_object_or_404(OptionService, id=id)

    if request.method == "POST":
        # Mise à jour des champs
        option.nom = request.POST["nom"]
        option.prix_supplementaire = Decimal(request.POST["prix_supplementaire"])
        option.description = request.POST.get("description")
        option.statut = request.POST.get("statut")  # <-- important

        option.save()

        # Redirection vers le détail de l’abonnement lié
        if option.abonnement:
            return redirect("abonnements:detail", option.abonnement.id)
        else:
            return redirect("abonnements:options_liste")

    # Affichage du formulaire avec les données existantes
    return render(request, "options/edit.html", {"option": option})

@gestionnaire_required
@login_required
def delete_option(request, id):
    option = get_object_or_404(OptionService, id=id)
    abonnement_id = option.abonnement.id if option.abonnement else None
    option_nom = option.nom
    option_id = option.id
    option.delete()
    
    # 🔒 AuditLog
    from accounts.models import AuditLog
    AuditLog.objects.create(
        utilisateur=request.user,
        action="Suppression",
        entite="OptionService",
        entite_id=option_id,
        details=f"Suppression de l'option {option_nom}"
    )

    if abonnement_id:
        return redirect("abonnements:detail", abonnement_id)
    return redirect("abonnements:liste_options")
