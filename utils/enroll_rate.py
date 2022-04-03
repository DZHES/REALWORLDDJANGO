from events.models import Review

def enroll_rate(enroll):
    enrolls = {}
    for review in Review.objects.filter(event=enroll.event):
        if enroll.user == review.user:
            enrolls[enroll] = review.rate
    return enrolls.get(enroll, 0)