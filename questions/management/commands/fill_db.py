import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from faker import Faker

from core.models import Profile
from questions.models import Answer, AnswerLike, Question, QuestionLike, Tag


class Command(BaseCommand):
    help = 'fill db with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = max(1, options['ratio'])
        fake = Faker('ru_RU')
        random.seed(42)

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        likes_count = ratio * 200

        self.stdout.write(self.style.NOTICE(f'ratio={ratio}'))
        self.stdout.write(self.style.NOTICE(f'users={users_count}, questions={questions_count}, answers={answers_count}, tags={tags_count}, likes={likes_count}'))

        User = get_user_model()

        with transaction.atomic():
            user_offset = User.objects.count()
            users = []
            for i in range(users_count):
                users.append(
                    User(
                        username=f'user_{user_offset + i + 1}',
                        email=fake.email(),
                    )
                )
            User.objects.bulk_create(users, batch_size=2000)
            users = list(User.objects.order_by('-id')[:users_count])

            profiles = []
            for u in users:
                profiles.append(Profile(user=u, nickname=fake.user_name(), rating=random.randint(0, 50000)))
            Profile.objects.bulk_create(profiles, ignore_conflicts=True, batch_size=2000)

            tag_offset = Tag.objects.count()
            tags = []
            for i in range(tags_count):
                name = f'{fake.word()}_{tag_offset + i + 1}'
                base_slug = slugify(name, allow_unicode=False)
                if not base_slug:
                    base_slug = f'tag-{tag_offset + i + 1}'
                tags.append(Tag(name=name, slug=base_slug[:64]))
            Tag.objects.bulk_create(tags, batch_size=2000)
            tags = list(Tag.objects.order_by('-id')[:tags_count])

            questions = []
            for _ in range(questions_count):
                questions.append(
                    Question(
                        title=fake.sentence(nb_words=8)[:255],
                        text=fake.text(max_nb_chars=500),
                        author=random.choice(users),
                        views_count=random.randint(0, 70000),
                    )
                )
            Question.objects.bulk_create(questions, batch_size=2000)
            questions = list(Question.objects.order_by('-id')[:questions_count])

            through = Question.tags.through
            rels = []
            for q in questions:
                for t in random.sample(tags, k=min(len(tags), random.randint(1, 3))):
                    rels.append(through(question_id=q.id, tag_id=t.id))
            through.objects.bulk_create(rels, ignore_conflicts=True, batch_size=5000)

            answers = []
            for _ in range(answers_count):
                answers.append(
                    Answer(
                        question=random.choice(questions),
                        author=random.choice(users),
                        text=fake.text(max_nb_chars=400),
                        is_correct=False,
                    )
                )
            Answer.objects.bulk_create(answers, batch_size=3000)
            answers = list(Answer.objects.order_by('-id')[:answers_count])

            q_likes = []
            a_likes = []
            for _ in range(likes_count):
                u = random.choice(users)
                if random.random() < 0.4:
                    q = random.choice(questions)
                    q_likes.append(
                        QuestionLike(
                            question_id=q.id,
                            user_id=u.id,
                            value=random.choice([QuestionLike.LIKE, QuestionLike.DISLIKE]),
                        )
                    )
                else:
                    a = random.choice(answers)
                    a_likes.append(
                        AnswerLike(
                            answer_id=a.id,
                            user_id=u.id,
                            value=random.choice([AnswerLike.LIKE, AnswerLike.DISLIKE]),
                        )
                    )
            QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True, batch_size=5000)
            AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True, batch_size=5000)

        self.stdout.write(self.style.SUCCESS('fill_db done'))
