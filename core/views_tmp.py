@comptable_required
@login_required
def generer_salaires_mensuels_view(request):
    """
    Génère les fiches de salaires 'Prévu' pour tous les agents actifs
    pour le mois en cours.
    """
    from django.db import transaction
    today = now().date()
    # On fixe la période au 1er du mois en cours pour la cohérence
    periode_debut = today.replace(day=1)
    count = 0

    with transaction.atomic():
        agents_actifs = Agent.objects.filter(statut=Agent.Statut.ACTIF)
        
        for agent in agents_actifs:
            # Vérifier si un salaire existe déjà pour cet agent et ce mois
            if not Salaire.objects.filter(agent=agent, periode=periode_debut).exists():
                Salaire.objects.create(
                    agent=agent,
                    montant=agent.salaire_base,
                    periode=periode_debut,
                    statut="Prévu"
                )
                count += 1

    if count > 0:
        messages.success(request, f"{count} fiches de salaires ont été générées pour le mois de {periode_debut.strftime('%B %Y')}.")
    else:
        messages.info(request, "Toutes les fiches de salaires pour ce mois existent déjà.")
        
    return redirect("dashboard:salaires")


@login_required
@comptable_required
def payer_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)

    if salaire.statut == "Payé":
        messages.warning(request, "Ce salaire est déjà payé.")
        return redirect("dashboard:salaires")

    # ✅ Mise à jour du statut et date
    salaire.statut = "Payé"
    salaire.date_versement = timezone.now().date()
    salaire.save()

    # ✅ Génération d’un reçu (optionnel)
    Recu.objects.create(
        paiement=None, 
        fichier_url=f"/media/recus/SAL-{salaire.id}.pdf",
        numero_recu=f"SAL-{salaire.id}",
        signature_comptable=request.user.get_full_name() or "Service Comptable"
    )

    messages.success(request, f"Le salaire de {salaire.agent} a été validé avec succès.")
    return redirect("dashboard:salaires")


@login_required
@role_required("Comptable")
def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            salaire = form.save(commit=False)
            # ✅ si statut = Payé, on met la date du jour
            if salaire.statut == "Payé" and not salaire.date_versement:
                from django.utils import timezone
                salaire.date_versement = timezone.now().date()
            salaire.save()
            return redirect("dashboard:salaires")
    else:
        form = SalaireForm()
    return render(request, "paiements/ajouter_salaire.html", {"form": form})
