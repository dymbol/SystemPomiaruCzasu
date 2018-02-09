def chosen_race(request):
    if request.user.is_authenticated and request.user.is_active:
        if 'chosen_race' in request.session.keys():
            return {'CHOSEN_RACE': request.session['chosen_race']}

