from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    if request.method=='POST':#ΕΛΕΝΧΕΙ ΑΜΑ Ο ΧΡΗΣΤΗΣ ΣΥΜΠΛΗΡΩΣΕ ΤΗΝ ΦΟΡΜΑ
        form=UserCreationForm(request.POST)#ΜΑΖΕΥΕΙ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΧΡΗΣΤΗ
        if form.is_valid():#ΕΛΕΝΧΟΣ ΔΕΔΟΜΕΝΩΝ
            form.save()#ΑΠΟΘΗΚΕΥΕΙ ΤΑ ΔΕΔΟΜΕΝΑ
            return redirect('login')#ΣΤΕΛΝΕΙ ΠΙΣΩ ΣΤΟ LOGIN PAGE
    else:
        form=UserCreationForm()#ΞΑΝΑΕΜΦΑΝΙΖΕΙ ΤΗΝ ΣΕΛΙΔΑ
    return render(request,'registration/register.html',{'form':form})#ΣΤΕΛΝΕΙ ΤΑ ΛΑΘΟΣ ΔΕΔΟΜΕΝΑ