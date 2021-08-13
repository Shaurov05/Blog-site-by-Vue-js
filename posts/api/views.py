from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.api.permissions import IsAuthorOrReadOnly
from posts.api.serializers import CommentSerializer, PostSerializer
from posts.models import Comment, Post


class PostViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Post."""
    queryset = Post.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpvoteAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        post.voters.add(user)
        post.vote = "upvote"
        post.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(post, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        post.voters.add(user)
        post.vote = "downvote"
        post.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(post, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(generics.CreateAPIView):
    """Allow users to Comment a Post instance if they haven't already."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=kwarg_slug)

        if post.comments.filter(author=request_user).exists():
            raise ValidationError("You have already commented this Post!")

        serializer.save(author=request_user, post=post)


class CommentListAPIView(generics.ListAPIView):
    """Provide the Comments queryset of a specific Post instance."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(post__slug=kwarg_slug).order_by("-created_at")


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an Comment instance to it's author."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CommentLikeAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        comment.voters.add(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        comment.voters.remove(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)




#
