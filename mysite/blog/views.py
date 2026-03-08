from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST


# Create your views here.


def post_list(request):
    post_list = Post.objects.all()  # ΤΡΑΒΑΕΙ ΟΛΑ ΤΑ POST
    paginator = Paginator(post_list, 3)  # ΔΙΧΝΕΙ ΑΝΑ 3 POST ΣΕ ΚΑΘΕ ΣΕΛΙΔΑ
    page_number = request.GET.get("page", 1)  # ΔΙΑΒΑΖΕΙ ΠΟΙΑ ΣΕΛΙΔΑ ΑΠΟ ΤΟ URL
    posts = paginator.get_page(page_number)  # ΦΕΡΝΕΙ ΤΑ ΑΡΘΡΑ ΤΗΣ ΣΕΛΙΔΑΣ
    return render(
        request, "blog/post/list.html", {"posts": posts}
    )  # ΣΤΕΛΝΕΙ ΤΑ POST ΣΤΟ HTML


def post_detail(request, year, month, day, post):  # ΚΑΛΗ ΤΟ ΣΥΓΚΕΚΡΙΜΕΝΟ POST
    post = get_object_or_404(
        Post, slug=post, publish__year=year, publish__month=month, publish__day=day
    )  # 404 Not Found
    comments = post.comments.filter(active=True)
    if request.method == "POST":  # ΑΝ ΑΠΟΣΤΕΙΛΕΙ ΣΧΟΛΙΟ
        form = CommentForm(data=request.POST)  # ΔΙΑΒΑΖΕΙ ΤΑ ΔΕΔΟΜΕΝΑ
        if form.is_valid():
            comment = form.save(commit=False)  # ΦΤΟΙΑΧΝΕΙ ΤΟ ΣΧΟΛΙΟ
            comment.post = post  # ΤΟ ΕΝΩΝΕΙ ΜΕ ΤΟ ΑΡΘΡΟ
            comment.save()  # ΤΟ ΑΠΟΘΗΚΕΥΕΙ
            form = CommentForm()  # ΑΡΧΙΚΟΠΟΙΗ ΤΟ ΦΟΡΜΑ
    else:
        form = CommentForm()  # ΑΡΧΙΚΟΠΟΙΗ ΤΟ ΦΟΡΜΑ

    form = CommentForm()
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
