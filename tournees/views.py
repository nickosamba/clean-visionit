from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournee, TourneeClient
from secteurs.models import Secteur
from agents.models import Agent
from clients.models import Client
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from core.decorators import agent_required, comptable_required, gestionnaire_required, admin_required
from django.contrib.auth.decorators import login_required
# --- Tournées ---

@gestionnaire_required
@login_required
def liste_tournees(request):
    search = request.GET.get("search", "")
    secteur_filter = request.GET.get("secteur", "")
    agent_filter = request.GET.get("agent", "")
    date_filter = request.GET.get("date", "")

    tournees = (
        Tournee.objects.select_related("secteur", "agent", "agent__user")
        .order_by("-date")
    )

    # 🔍 Recherche globale
    if search:
        tournees = tournees.filter(
            Q(agent__user__first_name__icontains=search)
            | Q(agent__user__last_name__icontains=search)
            | Q(secteur__nom__icontains=search)
        )

    # Filtre secteur
    if secteur_filter:
        tournees = tournees.filter(secteur_id=secteur_filter)

    # Filtre agent
    if agent_filter:
        tournees = tournees.filter(agent_id=agent_filter)

    # Filtre date
    if date_filter:
        tournees = tournees.filter(date=date_filter)

    # Pagination
    paginator = Paginator(tournees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tournees": page_obj,
        "page_obj": page_obj,
        "secteurs": Secteur.objects.all(),
        "agents": Agent.objects.select_related("user").all(),
        "search": search,
        "secteur_filter": secteur_filter,
        "agent_filter": agent_filter,
        "date_filter": date_filter,
    }
    return render(request, "tournees/liste.html", context)

@gestionnaire_required
@login_required
def create_tournee(request):
    secteurs = Secteur.objects.all()
    agents = Agent.objects.all()
    statut_choices = Tournee.Statut.choices   # 👈 on récupère les choix

    if request.method == "POST":
        secteur = get_object_or_404(Secteur, id=request.POST["secteur"])
        agent = get_object_or_404(Agent, id=request.POST["agent"])
        tournee = Tournee.objects.create(
            date=request.POST["date"],
            secteur=secteur,
            agent=agent,
            statut=request.POST.get("statut", Tournee.Statut.PLANIFIE),
            heure_debut=request.POST.get("heure_debut") or None,
            heure_fin=request.POST.get("heure_fin") or None,
            vehicule=request.POST.get("vehicule")
        )

        # Add a success message that will be used to trigger the notification
        from django.contrib import messages
        messages.success(request, f'Tournee créée avec succès pour l\'agent {agent.user.first_name} {agent.user.last_name} le {tournee.date}.')
        return redirect("tournees:tournees")

    return render(request, "tournees/create.html", {
        "secteurs": secteurs,
        "agents": agents,
        "statut_choices": statut_choices   # 👈 on envoie au template
    })

@gestionnaire_required
@login_required
def edit_tournee(request, id):
    tournee = get_object_or_404(Tournee, id=id)
    secteurs = Secteur.objects.all()
    agents = Agent.objects.all()
    if request.method == "POST":
        tournee.date = request.POST["date"]
        tournee.secteur = get_object_or_404(Secteur, id=request.POST["secteur"])
        tournee.agent = get_object_or_404(Agent, id=request.POST["agent"])
        tournee.statut = request.POST.get("statut", Tournee.Statut.PLANIFIE)
        tournee.heure_debut = request.POST.get("heure_debut") or None
        tournee.heure_fin = request.POST.get("heure_fin") or None
        tournee.vehicule = request.POST.get("vehicule")
        tournee.save()
        return redirect("tournees:tournees")
    return render(request, "tournees/edit.html", {"tournee": tournee, "secteurs": secteurs, "agents": agents})

@gestionnaire_required
@login_required
def delete_tournee(request, id):
    tournee = get_object_or_404(Tournee, id=id)
    tournee.delete()
    return redirect("tournees:tournees")


@gestionnaire_required
@login_required
def detail_tournee(request, id):
    tournee = get_object_or_404(Tournee, id=id)
    clients = tournee.clients.select_related("client").all()
    return render(request, "tournees/detail.html", {"tournee": tournee, "clients": clients})


# --- Clients associés à une tournée ---
@gestionnaire_required
@login_required
def liste_tournee_clients(request, tournee_id):
    tournee = get_object_or_404(Tournee, id=tournee_id)
    clients = tournee.clients.select_related("client").all()
    return render(request, "tournees/liste_clients.html", {"tournee": tournee, "clients": clients})

from .models import TourneeClient

@gestionnaire_required
@login_required
def add_tournee_client(request, tournee_id):
    tournee = get_object_or_404(Tournee, id=tournee_id)
    
    # 🔍 Sécurité : On ne propose que les clients du SECTEUR de la tournée
    # ET qui ne sont pas déjà planifiés pour cette DATE précise (toutes tournées confondues)
    clients_deja_planifies = TourneeClient.objects.filter(
        tournee__date=tournee.date
    ).values_list('client_id', flat=True)
    
    clients = Client.objects.filter(
        rue__secteur=tournee.secteur
    ).exclude(id__in=clients_deja_planifies)
    
    statut_choices = TourneeClient.StatutService.choices

    if request.method == "POST":
        client_id = request.POST.get("client")
        if not client_id:
            from django.contrib import messages
            messages.error(request, "Veuillez sélectionner un client.")
            return redirect("tournees:add_client", tournee_id=tournee.id)

        client = get_object_or_404(Client, id=client_id)
        
        # Double vérification de sécurité côté serveur
        if TourneeClient.objects.filter(tournee__date=tournee.date, client=client).exists():
            from django.contrib import messages
            messages.error(request, f"Le client {client.nom} est déjà planifié dans une tournée pour le {tournee.date}.")
            return redirect("tournees:liste_clients", tournee_id=tournee.id)

        TourneeClient.objects.create(
            tournee=tournee,
            client=client,
            statut_service=request.POST.get("statut_service", TourneeClient.StatutService.PLANIFIE),
            commentaires_agent=request.POST.get("commentaires_agent")
        )

        from django.contrib import messages
        messages.success(request, f'Client {client.nom} ajouté à la tournée #{tournee.id}.')
        return redirect("tournees:liste_clients", tournee_id=tournee.id)

    return render(request, "tournees/add_client.html", {
        "tournee": tournee,
        "clients": clients,
        "statut_choices": statut_choices
    })

@gestionnaire_required
@login_required
@require_POST
def add_sector_clients_to_tournee(request, tournee_id):
    """
    IMPORT MASSIF : Ajoute tous les clients du secteur à la tournée en un clic,
    en évitant ceux déjà planifiés ailleurs.
    """
    tournee = get_object_or_404(Tournee, id=tournee_id)
    
    # Clients déjà planifiés ce jour-là
    clients_deja_planifies = TourneeClient.objects.filter(
        tournee__date=tournee.date
    ).values_list('client_id', flat=True)
    
    # Clients du secteur non encore planifiés
    clients_a_ajouter = Client.objects.filter(
        rue__secteur=tournee.secteur,
        statut=Client.Statut.ACTIF
    ).exclude(id__in=clients_deja_planifies)
    
    count = 0
    for client in clients_a_ajouter:
        TourneeClient.objects.create(
            tournee=tournee,
            client=client,
            statut_service=TourneeClient.StatutService.PLANIFIE
        )
        count += 1
    
    from django.contrib import messages
    if count > 0:
        messages.success(request, f"{count} clients du secteur {tournee.secteur.nom} ont été ajoutés à la tournée.")
    else:
        messages.warning(request, "Aucun client supplémentaire n'a pu être ajouté (déjà planifiés ou aucun client actif).")
        
    return redirect("tournees:liste_clients", tournee_id=tournee.id)

@gestionnaire_required
@login_required
def edit_tournee_client(request, id):
    tc = get_object_or_404(TourneeClient, id=id)
    if request.method == "POST":
        tc.statut_service = request.POST.get("statut_service", tc.statut_service)
        tc.commentaires_agent = request.POST.get("commentaires_agent")
        tc.save()
        return redirect("tournees:liste_clients", tournee_id=tc.tournee.id)
    return render(request, "tournees/edit_client.html", {"tc": tc})

@gestionnaire_required
@login_required
def delete_tournee_client(request, id):
    tc = get_object_or_404(TourneeClient, id=id)
    tournee_id = tc.tournee.id
    tc.delete()
    return redirect("tournees:liste_clients", tournee_id=tournee_id)

