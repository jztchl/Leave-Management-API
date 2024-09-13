from .models import leavelist

def reset_leaves():
    leavelist.objects.update(paidleave=0, unpaidleave=0)
    print("Leave list has been reset!")

