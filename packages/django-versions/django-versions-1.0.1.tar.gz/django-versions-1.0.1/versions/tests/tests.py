from __future__ import with_statement

import random
import shutil
import threading
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.test import TestCase

from versions.base import revision
from versions.exceptions import VersionDoesNotExist, VersionsException, VersionsManagementException
from versions.tests.models import Artist, Album, Song, Lyrics, Venue

class VersionsTestCase(TestCase):
    def setUp(self):
        for key, configs in settings.VERSIONS_REPOSITORIES.items():
            shutil.rmtree(configs['local'], ignore_errors=True)

    def tearDown(self):
        for key, configs in settings.VERSIONS_REPOSITORIES.items():
            shutil.rmtree(configs['local'], ignore_errors=True)

class VersionsModelTestCase(VersionsTestCase):
    def test_unmanaged_edits(self):
        queen = Artist(name='Queen')
        self.assertRaises(VersionsManagementException, queen.save)

    def test_managed_edits(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()
            self.assertEquals(len(Artist.objects.versions(queen)), 0)

            prince = Artist(name='Prince')
            prince.save()
            self.assertEquals(len(Artist.objects.versions(prince)), 0)

            prince.name = 'The Artist Formerly Known As Prince'
            prince.save()

            self.assertEquals(len(Artist.objects.versions(prince)), 0)

            prince.name = 'Prince'
            prince.save()

            self.assertEquals(len(Artist.objects.versions(prince)), 0)

            # Finish the versioning session.

        # Verify that we have only commited once for all of the edits.
        self.assertEquals(len(Artist.objects.versions(prince)), 1)
        self.assertEquals(len(Artist.objects.versions(queen)), 1)

        # Verify that both edits to Queen and Prince were tracked in the same revision.
        self.assertEquals(Artist.objects.versions(prince), Artist.objects.versions(queen))

    def test_related_model_edits(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

            dont_lose_your_head = Song(album=a_kind_of_magic, title="Don't Lose Your Head")
            dont_lose_your_head.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            princes_of_the_universe = Song(album=a_kind_of_magic, title='Princes of the Universe')
            princes_of_the_universe.save()

            dont_lose_your_head.seconds = 278
            dont_lose_your_head.save()

        second_revision = revision.latest_transactions['default']

        with revision:
            princes_of_the_universe.seconds = 212
            princes_of_the_universe.save()

            friends_will_be_friends = Song(album=a_kind_of_magic, title='Friends Will Be Friends')
            friends_will_be_friends.save()

        third_revision = revision.latest_transactions['default']

        with revision:
            # the a_kind_of_magic album was not modified after the initial commit. Verify that we can retrieve the a_kind_of_magic model from the various versions
            first_a_kind_of_magic = Album.objects.version(first_revision).get(pk=a_kind_of_magic.pk)
            second_a_kind_of_magic = Album.objects.version(second_revision).get(pk=a_kind_of_magic.pk)
            third_a_kind_of_magic = Album.objects.version(third_revision).get(pk=a_kind_of_magic.pk)

            # Verify that the data is the same.
            self.assertEqual(revision.data(first_a_kind_of_magic)['field'], revision.data(second_a_kind_of_magic)['field'])
            self.assertEqual(revision.data(second_a_kind_of_magic)['field'], revision.data(third_a_kind_of_magic)['field'])

            # Verify that princes_of_the_universe does not exist at the first_revision (it was created on the second revision)
            self.assertRaises(ObjectDoesNotExist, first_a_kind_of_magic.songs.get, pk=princes_of_the_universe.pk)

            # Verify that retrieving the object from the reverse relationship and directly from the Song objects yield the same result.
            self.assertEqual(second_a_kind_of_magic.songs.get(pk=princes_of_the_universe.pk).__dict__, Song.objects.version(second_revision).get(pk=princes_of_the_universe.pk).__dict__)

            # Verify that retrieval of the object from the reverse relationship return the correct versions of the objects.
            second_princes_of_the_universe = second_a_kind_of_magic.songs.get(pk=princes_of_the_universe.pk)
            self.assertEqual(second_princes_of_the_universe.seconds, None)

            third_princes_of_the_universe = third_a_kind_of_magic.songs.get(pk=princes_of_the_universe.pk)
            self.assertEqual(third_princes_of_the_universe.seconds, 212)

            # Verify that the first revision of a_kind_of_magic has one song
            self.assertEquals(len(first_a_kind_of_magic.songs.all()), 1)

            # Verify that the second revision of a_kind_of_magic has two songs
            self.assertEquals(len(second_a_kind_of_magic.songs.all()), 2)

            # Verify that the third revision of a_kind_of_magic has three songs
            self.assertEquals(len(third_a_kind_of_magic.songs.all()), 3)

    def test_revision_retrieval(self):
        with revision:
            prince = Artist(name='Prince')
            prince.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            prince.name = 'The Artist Formerly Known As Prince'
            prince.save()

        second_revision = revision.latest_transactions['default']

        with revision:
            prince.name = 'Prince'
            prince.save()

        third_revision = revision.latest_transactions['default']

        first_prince = Artist.objects.version(first_revision).get(pk=prince.pk)
        self.assertEquals(first_prince.name, 'Prince')
        self.assertEquals(first_prince._versions_revision, first_revision)

        second_prince = Artist.objects.version(second_revision).get(pk=prince.pk)
        self.assertEquals(second_prince.name, 'The Artist Formerly Known As Prince')
        self.assertEquals(second_prince._versions_revision, second_revision)

        third_prince = Artist.objects.version(third_revision).get(pk=prince.pk)
        self.assertEquals(third_prince.name, 'Prince')
        self.assertEquals(third_prince._versions_revision, third_revision)

    def test_deletion(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

            dont_lose_your_head = Song(album=a_kind_of_magic, title="Don't Lose Your Head")
            dont_lose_your_head.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            princes_of_the_universe = Song(album=a_kind_of_magic, title='Princes of the Universe')
            princes_of_the_universe.save()

            dont_lose_your_head.delete()

        second_revision = revision.latest_transactions['default']

        with revision:
            friends_will_be_friends = Song(album=a_kind_of_magic, title='Friends Will Be Friends')
            friends_will_be_friends.save()

        third_revision = revision.latest_transactions['default']

        self.assertEqual(Song.objects.version(first_revision).get(pk=dont_lose_your_head.pk), dont_lose_your_head)
        self.assertRaises(Song.DoesNotExist, Song.objects.version(second_revision).get, pk=dont_lose_your_head.pk)
        self.assertRaises(Song.DoesNotExist, Song.objects.version(third_revision).get, pk=dont_lose_your_head.pk)
        self.assertRaises(Song.DoesNotExist, Song.objects.get, pk=dont_lose_your_head.pk)
        self.assertEqual(list(Album.objects.version(first_revision).get(pk=a_kind_of_magic.pk).songs.all()), [dont_lose_your_head])
        self.assertEqual(list(Album.objects.version(second_revision).get(pk=a_kind_of_magic.pk).songs.all()), [princes_of_the_universe])
        self.assertEqual(list(Album.objects.version(third_revision).get(pk=a_kind_of_magic.pk).songs.all()), [princes_of_the_universe, friends_will_be_friends])

    def test_disabled_functions(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            prince = Artist(name='Price')
            prince.save()

        self.assertEqual(Artist.objects.count(), 2)
        self.assertRaises(VersionsException, Artist.objects.version('tip').count)
        self.assertRaises(VersionsException, Artist.objects.version('tip').aggregate)
        self.assertRaises(VersionsException, Artist.objects.version('tip').annotate)
        self.assertRaises(VersionsException, Artist.objects.version('tip').values_list)

    def test_many_to_many_fields(self):
        fan1 = User(username='fan1', email='fan1@example.com')
        fan1.save()

        fan2 = User(username='fan2', email='fan2@example.com')
        fan2.save()

        fan3 = User(username='fan3', email='fan3@example.com')
        fan3.save()

        with revision:
            queen = Artist(name='Queen')
            queen.save()
            queen.fans.add(fan1)

        first_revision = revision.latest_transactions['default']

        with revision:
            queen.fans = [fan2, fan3]

        second_revision = revision.latest_transactions['default']

        self.assertEqual(list(Artist.objects.version(first_revision).get(pk=queen.pk).fans.all()), [fan1])
        self.assertEqual(list(Artist.objects.version(second_revision).get(pk=queen.pk).fans.all()), [fan2, fan3])


    def test_many_to_many_versioned_update(self):
        fan1 = User(username='fan1', email='fan1@example.com')
        fan1.save()

        fan2 = User(username='fan2', email='fan2@example.com')
        fan2.save()

        with revision:
            Artist(name='Queen').save()

        with revision:
            queen = Artist.objects.version('tip').get(name='Queen')
            queen.fans.add(fan1)

        first_revision = revision.latest_transactions['default']

        with revision:
            queen.fans = [fan2]

        second_revision = revision.latest_transactions['default']

        self.assertEqual(list(Artist.objects.version(first_revision).get(pk=queen.pk).fans.all()), [fan1])
        self.assertEqual(list(Artist.objects.version(second_revision).get(pk=queen.pk).fans.all()), [fan2])

    def test_reverse_foreign_keys(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

            journey_album = Album(artist=queen, title='Journey')
            journey_album.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            journey = Artist(name='Journey')
            journey.save()

            journey_album.artist = journey
            journey_album.save()

        second_revision = revision.latest_transactions['default']

        self.assertEqual(list(Artist.objects.version(first_revision).get(pk=queen.pk).albums.all()), [a_kind_of_magic, journey_album])
        self.assertEqual(list(Artist.objects.version(second_revision).get(pk=queen.pk).albums.all()), [a_kind_of_magic])

class PublishedModelTestCase(VersionsTestCase):
    def test_staged_edits(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

            princes_of_the_universe = Song(album=a_kind_of_magic, title='Princes of the Universe')
            princes_of_the_universe.save()

            dont_lose_your_head = Song(album=a_kind_of_magic, title="Don't Lose Your Head")
            dont_lose_your_head.save()

            original_lyrics = Lyrics(song=dont_lose_your_head, text="Dont lose your head")
            original_lyrics.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            queen.stage()
            a_kind_of_magic.stage()
            princes_of_the_universe.stage()
            dont_lose_your_head.stage()

            new_lyrics = """Dont lose your head
Dont lose your head
Dont lose your head
No dont lose you head
"""

            staged_edits_lyrics = Lyrics.objects.version('tip').get(pk=original_lyrics.pk)
            staged_edits_lyrics.text = new_lyrics
            staged_edits_lyrics.stage()

            princes_of_the_universe.delete()

        second_revision = revision.latest_transactions['default']

        # Ensure the database version still points to the old lyrics.
        self.assertEquals(Lyrics.objects.get(pk=original_lyrics.pk).text, "Dont lose your head")
        self.assertEquals(list(Album.objects.get(pk=a_kind_of_magic.pk).songs.all()), [princes_of_the_universe, dont_lose_your_head])
        # Ensure that the versions contain the correct information.
        self.assertEquals(Lyrics.objects.version(first_revision).get(pk=original_lyrics.pk).text, "Dont lose your head")
        self.assertEquals(Lyrics.objects.version(second_revision).get(pk=original_lyrics.pk).text, new_lyrics)

        with revision:
            queen.commit()
            a_kind_of_magic.commit()
            Album.objects.version('tip').get(pk=a_kind_of_magic.pk).songs.commit()

            new_lyrics = """Dont lose your head
Dont lose your head
Dont lose your head
Dont lose your head
No dont lose you head
Dont lose you head
Hear what I say
Dont lose your way - yeah
Remember loves stronger remember love walks tall
"""

            published_lyrics = Lyrics.objects.version('tip').get(pk=original_lyrics.pk)
            published_lyrics.text = new_lyrics
            published_lyrics.commit()

        third_revision = revision.latest_transactions['default']

        # Ensure the database version points to the new lyrics.
        self.assertEquals(Lyrics.objects.get(pk=original_lyrics.pk).text, new_lyrics)
        # Ensure the database version only has on song. Princess of the universe has been deleted.
        self.assertEquals(list(Album.objects.get(pk=a_kind_of_magic.pk).songs.all()), [dont_lose_your_head])
        # Ensure that the versions contain the correct information.
        self.assertEquals(Lyrics.objects.version(third_revision).get(pk=original_lyrics.pk).text, new_lyrics)

    def test_staged_edits_new(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

            dont_lose_your_head = Song(album=a_kind_of_magic, title="Don't Lose Your Head")
            dont_lose_your_head.save()

            princes_of_the_universe = Song(album=a_kind_of_magic, title='Princes of the Universe')
            princes_of_the_universe.save()

            original_lyrics = Lyrics(song=princes_of_the_universe, text="Dont lose your head")
            original_lyrics.stage()

        first_revision = revision.latest_transactions['default']

        with revision:
            original_lyrics.song = dont_lose_your_head
            original_lyrics.stage()

        second_revision = revision.latest_transactions['default']

        # Verify that the lyrics object does not exist from the published perspective.
        self.assertRaises(Lyrics.DoesNotExist, Lyrics.objects.get, pk=original_lyrics.pk)
        # Vefify that the the published Song object does not know that the new lyrics exist.
        self.assertEquals(list(Song.objects.get(pk=princes_of_the_universe.pk).lyrics.all()), [])

        # Verify that the first staged version of the Song object knows that the lyrics exist.
        self.assertEquals(list(Song.objects.version(first_revision).get(pk=princes_of_the_universe.pk).lyrics.all()), [original_lyrics])
        # Verify that the first staged version of the Song object knows that the lyrics exist.
        self.assertEquals(list(Song.objects.version(first_revision).get(pk=dont_lose_your_head.pk).lyrics.all()), [])

        # Verify that the second staged version of the Song object knows that the lyrics do not exist because they were altered to point to the correct song.
        self.assertEquals(list(Song.objects.version(second_revision).get(pk=princes_of_the_universe.pk).lyrics.all()), [])
        # Verify that the second staged version of the Song object knows that the lyrics do not exist because they were altered to point to the correct song.
        self.assertEquals(list(Song.objects.version(second_revision).get(pk=dont_lose_your_head.pk).lyrics.all()), [original_lyrics])

        with revision:
            original_lyrics.commit()

        third_revision = revision.latest_transactions['default']

        self.assertEquals(Lyrics.objects.get(pk=original_lyrics.pk), original_lyrics)

    def test_staged_edits_many_to_many(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            venue = Venue(name='Home')
            venue.save()

        first_revision = revision.latest_transactions['default']

        with revision:
            venue.stage()
            venue.artists.add(queen)

        second_revision = revision.latest_transactions['default']

        self.assertEquals(list(Venue.objects.get(pk=venue.pk).artists.all()), [])
        self.assertEquals(list(Venue.objects.version(second_revision).get(pk=venue.pk).artists.all()), [queen])

        self.assertEquals(list(Artist.objects.get(pk=queen.pk).venues.all()), [])
        self.assertEquals(list(Artist.objects.version(second_revision).get(pk=queen.pk).venues.all()), [venue])

        with revision:
            venue = Venue.objects.version(second_revision).get(pk=venue.pk)
            venue.commit()

        third_revision = revision.latest_transactions['default']

        self.assertEquals(list(Venue.objects.get(pk=venue.pk).artists.all()), [queen])
        self.assertEquals(list(Venue.objects.version(third_revision).get(pk=venue.pk).artists.all()), [queen])

        self.assertEquals(list(Artist.objects.get(pk=queen.pk).venues.all()), [venue])
        self.assertEquals(list(Artist.objects.version(third_revision).get(pk=queen.pk).venues.all()), [venue])

        with revision:
            venue = Venue.objects.version(third_revision).get(pk=venue.pk)
            venue.stage()
            venue.artists.clear()

        fourth_revision = revision.latest_transactions['default']

        self.assertEquals(list(Venue.objects.get(pk=venue.pk).artists.all()), [queen])
        self.assertEquals(list(Venue.objects.version(fourth_revision).get(pk=venue.pk).artists.all()), [])

        self.assertEquals(list(Artist.objects.get(pk=queen.pk).venues.all()), [venue])
        self.assertEquals(list(Artist.objects.version(fourth_revision).get(pk=queen.pk).venues.all()), [])

        with revision:
            venue = Venue.objects.version(fourth_revision).get(pk=venue.pk)
            venue.commit()

        fifth_revision = revision.latest_transactions['default']

        self.assertEquals(list(Venue.objects.get(pk=venue.pk).artists.all()), [])
        self.assertEquals(list(Venue.objects.version(fifth_revision).get(pk=venue.pk).artists.all()), [])

        self.assertEquals(list(Artist.objects.get(pk=queen.pk).venues.all()), [])
        self.assertEquals(list(Artist.objects.version(fourth_revision).get(pk=queen.pk).venues.all()), [])

class VersionsOptionsTestCase(VersionsTestCase):
    def test_field_exclude(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

        data = revision.data(queen)
        self.assertEqual(data['field'].keys(), ['_versions_status', 'name'])

    def test_field_include(self):
        with revision:
            queen = Artist(name='Queen')
            queen.save()

            a_kind_of_magic = Album(artist=queen, title='A Kind of Magic')
            a_kind_of_magic.save()

        data = revision.data(a_kind_of_magic)
        self.assertEqual(data['field'].keys(), ['_versions_status', 'title'])

class VersionsThreadedTestCase(VersionsTestCase):
    def test_concurrent_edits(self):
        @transaction.commit_on_success
        @revision.commit_on_success
        def concurrent_edit():
            try:
                queen, is_new = Artist.objects.version('tip').get_or_create(pk=1, defaults={'name': 'Queen'})
                if not is_new:
                    queen.name = 'Queen (%s)' % random.randint(0, 1000)
                    queen.save()
            except:
                pass

        thread = threading.Thread(target=concurrent_edit)
        thread.start()
        thread.join()

        NUM_THREADS = 10
        threads = []
        for x in xrange(1, NUM_THREADS):
            thread = threading.Thread(target=concurrent_edit)
            threads.append(thread)
            thread.start()

        alive = True
        while alive:
            alive = False
            for thread in threads:
                alive = alive or thread.isAlive()

        queen = Artist.objects.get(pk=1)
        versions = list(reversed(list(Artist.objects.versions(queen))))

        self.assertEqual(len(versions), NUM_THREADS)

        previous_version = versions[0].parent
        # Ensure our base commit is the 000000000000000000000000000 commit.
        self.assertEqual(previous_version.revision, ''.zfill(len(previous_version.revision)))
        for version in versions:
            parents = list(version.parents)
            # Ensure that we only have one parent
            self.assertEqual(len(parents), 1)
            # Ensure that the the parent revision is that of the previous revision (we want a linear revision history).
            self.assertEqual(version.parent.revision, previous_version.revision)
            previous_version = version
