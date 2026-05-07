from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import TourneeClient
import json
from django.utils import timezone
from django.core.serializers import serialize
from django.forms.models import model_to_dict


@login_required
def check_new_assignments(request):
    """
    API endpoint to check for new assignments for the current agent
    """
    if request.user.role != "Agent de terrain":
        return JsonResponse({"error": "Access denied"}, status=403)
    
    # Get the agent associated with this user
    try:
        agent = request.user.agent
    except:
        return JsonResponse({"assignments": []})
    
    # Get tournees for this agent from today onwards
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.now().date()
    
    # Get tournee clients assigned to this agent's tournees
    # Only get assignments created in the last 24 hours to avoid duplicates
    from django.utils import timezone
    from datetime import timedelta
    time_threshold = timezone.now() - timedelta(hours=24)

    assignments = TourneeClient.objects.filter(
        tournee__agent=agent,
        created_at__gte=time_threshold
    ).select_related('tournee', 'client').order_by('-created_at')
    
    # Prepare data to return
    assignments_data = []
    for assignment in assignments[:10]:  # Return last 10 assignments
        assignments_data.append({
            'id': assignment.id,
            'client_name': assignment.client.nom,
            'tournee_date': assignment.tournee.date.isoformat() if assignment.tournee.date else None,
            'created_at': assignment.created_at.isoformat(),
            'statut_service': assignment.statut_service
        })
    
    return JsonResponse({"assignments": assignments_data})