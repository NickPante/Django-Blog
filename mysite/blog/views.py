from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils import timezone  # <-- ΠΡΟΣΘΗΚΗ ΓΙΑ ΤΗΝ ΗΜΕΡΟΜΗΝΙΑ/ΩΡΑ

from .models import Post
from .forms import EmailPostForm, CommentForm, PostCreateForm


# Create your views here.


def post_list(request):
    post_list = Post.objects.all()  # ΤΡΑΒΑΕΙ ΟΛΑ ΤΑ POST
    paginator = Paginator(post_list, 3)  # ΔΙΧΝΕΙ ΑΝΑ 3 POST ΣΕ ΚΑΘΕ ΣΕΛΙΔΑ
    page_number = request.GET.get("page", 1)  # ΔΙΑΒΑΖΕΙ ΠΟΙΑ ΣΕΛΙΔΑ ΑΠΟ ΤΟ URL
    posts = paginator.get_page(page_number)  # ΦΕΡΝΕΙ ΤΑ ΑΡΘΡΑ ΤΗΣ ΣΕΛΙΔΑΣ
    return render(
        request, "blog/post/list.html", {"posts": posts}
    )  # ΣΤΕΛΝΕΙ ΤΑ POST ΣΤΟ HTML


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )  # ΨΑΧΝΕΙ ΤΟ POST
    comments = post.comments.filter(active=True)  # ΔΕΧΕΤΑΙ ΤΑ ΕΝΕΡΓΑ POST
    form = CommentForm()  # ΔΗΜΙΟΥΡΓΙΑ ΜΙΑΣ ΦΟΡΜΑ ΜΕ ΤΑ COMMENT ΠΟΥ ΣΤΕΛΝΕΤΑΙ ΣΤΑ HTML
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if (
        request.method == "POST"
    ):  # ΓΙΑ ΝΑ ΕΙΝΑΙ POST ΣΗΜΕΝΕΙ ΟΤΙ Ο ΧΡΗΣΤΗΣ ΣΥΜΠΛΗΡΩΣΕ ΤΗΝ ΦΟΡΜΑ
        form = EmailPostForm(request.POST)  # ΔΗΜΙΟΥΡΓΟ ΤΗΝ ΦΟΡΜΑ
        if form.is_valid():  # ΤΗΝ ΕΛΕΝΧΩ
            cd = form.cleaned_data  # ΜΕΤΑΤΡΟΠΕΙ ΔΕΔΟΜΕΝΩΝ ΣΕ ΕΠΙΤΡΕΠΤΕΣ ΤΙΜΕΣ
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )  # ΤΟ LINK ΠΟΥ ΣΤΕΛΝΩ
            subject = f"{cd['name']} recommends {post.title}"  # ΤΙΤΛΟΣ
            message = f"Read {post.title} at {post_url}\n\nComments: {cd['comments']}"  # ΚΕΙΜΕΝΟΥ
            send_mail(
                subject, message, "admin@myblog.com", [cd["to"]]
            )  # ΣΥΝΘΕΣΗ ΤΟΥ ΚΕΙΜΕΝΟΥ ΚΑΙ ΤΙΤΛΟΥ ΤΩΝ ΔΕΔΟΜΕΝΩΝ
            sent = True  # FLAG
        else:
            form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST  # ΚΑΝΕΙ ΤΗΝ ΑΛΛΑΓΗ ΜΟΝΟ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ ΚΟΥΜΠΙΟΥ
def post_comment(request, post_id):
    post = get_object_or_404(
        Post, id=post_id, status=Post.Status.PUBLISHED
    )  # ΨΑΧΝΕΙ ΤΟ POST ΜΕΣΩ ΤΟΥ ID
    comment = None
    form = CommentForm(data=request.POST)  # ΦΟΡΜ ΔΕΔΟΜΕΝΩΝ ΤΟΥ ΧΡΗΣΤΗ
    if form.is_valid():  # ΕΛΕΝΧΩ ΤΑ ΔΕΔΟΜΕΝΑ ΑΝ ΕΙΝΑΙ ΣΩΣΤΑ
        comment = form.save(commit=False)  # ΦΤΟΙΑΧΝΩ ΤΟ ΣΧΟΛΙΟ
        comment.post = post  # ΚΑΡΦΙΤΣΩΝΩ ΤΟ ΣΧΟΛΙΟ ΣΤΟ POST
        comment.save()  # ΤΟ ΑΠΟΘΗΚΕΥΩ ΣΤΗΝ ΒΑΣΗ
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )  # ΤΟ ΕΠΙΣΤΡΕΦΕΙ ΣΤΗΝ HTML


@login_required  # ΕΠΙΤΡΕΠΕΙ ΤΗΝ ΠΡΟΣΒΑΣΗ ΜΟΝΟ ΣΕ ΣΥΝΔΕΔΕΜΕΝΟΥΣ ΧΡΗΣΤΕΣ
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ΣΥΝΔΕΕΙ ΤΟ POST ΜΕ ΤΟΝ ΣΥΝΔΕΔΕΜΕΝΟ ΧΡΗΣΤΗ
            post.slug = slugify(post.title)  # ΔΗΜΙΟΥΡΓΕΙ ΤΟ SLUG ΑΠΟ ΤΟΝ ΤΙΤΛΟ
            post.status = Post.Status.PUBLISHED  # ΟΡΙΖΕΙ ΤΟ POST ΩΣ ΔΗΜΟΣΙΕΥΜΕΝΟ
            post.publish = timezone.now()  # ΟΡΙΖΕΙ ΤΗΝ ΗΜΕΡΟΜΗΝΙΑ/ΩΡΑ ΔΗΜΟΣΙΕΥΣΗΣ
            post.save()  # ΑΠΟΘΗΚΕΥΕΙ ΤΟ POST ΣΤΗ ΒΑΣΗ
            form.save_m2m()  # ΑΠΑΡΑΙΤΗΤΟ ΓΙΑ ΤΗΝ ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ TAGS (MANY-TO-MANY)
            return redirect(post.get_absolute_url())  # ΑΝΑΚΑΤΕΥΘΥΝΣΗ ΣΤΟ ΑΡΘΡΟ ΠΟΥ ΜΟΛΙΣ ΦΤΙΑΧΤΗΚΕ
    else:
        form = PostCreateForm()

    return render(request, "create.html", {"form": form})