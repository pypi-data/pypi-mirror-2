import operator
import collections
import datetime
import simplejson
from .enums import RACE, CLASS, QUALITY, RACE_TO_FACTION
from .utils import make_icon_url, normalize, make_connection

__all__ = ['Character', 'Guild', 'Realm']

class Thing(object):
    def to_json(self):
        return simplejson.dumps(getattr(self, '_data'))

    def __repr__(self):
        return '<%s>' % (self.__class__.__name__,)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return getattr(self, '_data') == getattr(other, '_data')

    def __ne__(self, other):
        return not self.__eq__(other)
    
class Character(Thing):
    MALE = 'male'
    FEMALE = 'female'

    ALLIANCE = 'Alliance'
    HORDE = 'Horde'

    DRAENEI = 'Draenei'
    DWARF = 'Dwarf'
    GNOME = 'Gnome'
    HUMAN = 'Human'
    NIGHT_ELF = 'Nihgt Elf'
    WORGEN = 'Worgen'

    BLOOD_ELF = 'Blood Elf'
    UNDEAD = 'Undead'
    GOBLIN = 'Goblin'
    ORC = 'Orc'
    TAUREN = 'Tauren'
    TROLL = 'Troll'

    DEATH_KNIGHT = 'Death Knight'
    DRUID = 'Druid'
    HUNTER = 'Hunter'
    MAGE = 'Mage'
    PALADIN = 'Paladin'
    PRIEST = 'Priest'
    ROGUE = 'Rogue'
    SHAMAN = 'Shaman'
    WARLOCK = 'Warlock'
    WARRIOR = 'Warrior'

    ALCHEMY = 'Alchemy'
    BLACKSMITHING = 'Blacksmithing'
    ENCHANTING = 'Enchanting'
    ENGINEERING = 'Engineering'
    HERBALISM = 'Herbalism'
    INSCRIPTION = 'Inscription'
    JEWELCRATING = 'Jewelcrafting'
    LEATHERWORKING = 'Leatherworking'
    MINING = 'Mining'
    Skinning = 'Skinning'
    TAILORING = 'Tailoring'

    ARCHAEOLOGY = 'Archaeology'
    COOKING = 'Cooking'
    FIRST_AID = 'First Aid'
    FISHING = 'Fishing'

    STATS = 'stats'
    TALENTS = 'talents'
    ITEMS = 'items'
    REPUTATIONS = 'reputation'
    TITLES = 'titles'
    PROFESSIONS = 'professions'
    APPEARANCE = 'appearance'
    COMPANIONS = 'companions'
    MOUNTS = 'mounts'
    GUILD = 'guild'
    ALL_FIELDS = [STATS, TALENTS, ITEMS, REPUTATIONS, TITLES, PROFESSIONS, APPEARANCE, COMPANIONS, MOUNTS, GUILD]

    def __init__(self, region, realm=None, name=None, data=None, fields=None, connection=None):
        self.region = region
        self.connection = connection or make_connection()

        self._fields = set(fields or [])

        if realm and name and not data:
            data = self.connection.get_character(region, realm, name, raw=True, fields=self._fields)

        self.populate(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s@%s>' % (self.__class__.__name__, self.name, self.realm)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        
        return self.connection == other.connection \
            and self.name == other.name \
            and self.get_realm_name() == other.get_realm_name()

    def _refresh_if_not_present(self, field):
        if not hasattr(self, '_' + field):
            if field not in self._data:
                self.refresh(field)

            return True
        
    def populate(self, data):
        self._data = data

        self.name = normalize(data['name'])
        self.level = data['level']
        self.class_ = data['class']
        self.race = data['race']
        self.thumbnail = data['thumbnail']
        self.gender = data['gender']
        self.last_modified = datetime.datetime.fromtimestamp(data['lastModified'] / 1000)
        self.achievement_points = data['achievementPoints']
        self.faction = RACE_TO_FACTION[self.race]

        if 'pets' in data:
            self.pets = [Pet(pet) for pet in self._data['pets']]

    @property
    def realm(self):
        if not hasattr(self, '_realm'):
            self._realm = Realm(self.region, self._data['realm'], connection=self.connection)

        return self._realm

    @property
    def professions(self):
        if self._refresh_if_not_present(Character.PROFESSIONS):
            professions = {
                'primary': [],
                'secondary': []
            }

            for type_ in professions.keys():
                 professions[type_] = [Profession(self, profession)
                     for profession in self._data[Character.PROFESSIONS][type_]]

            self._professions = professions

        return self._professions

    @property
    def equipment(self):
        if self._refresh_if_not_present(Character.ITEMS):
            self._items = Equipment(self, self._data[Character.ITEMS])
            
        return self._items

    @property
    def mounts(self):
        if self._refresh_if_not_present(Character.MOUNTS):
            self._mounts = list(self._data[Character.MOUNTS])

        return self._mounts

    @property
    def companions(self):
        if self._refresh_if_not_present(Character.COMPANIONS):
            self._companions = list(self._data[Character.COMPANIONS])

        return self._companions

    @property
    def reputations(self):
        if self._refresh_if_not_present(Character.REPUTATIONS):
            self._reputation = [Reputation(reputation) for reputation in self._data[Character.REPUTATIONS]]

        return self._reputation

    @property
    def titles(self):
        if self._refresh_if_not_present(Character.TITLES):
            self._titles = [Title(self, title) for title in self._data[Character.TITLES]]

        return self._titles

    @property
    def guild(self):
        if self._refresh_if_not_present(Character.GUILD):
            self._guild = Guild(self.region, data=self._data[Character.GUILD], connection=self.connection)

        return self._guild

    @property
    def appearance(self):
        if self._refresh_if_not_present(Character.APPEARANCE):
            self._appearance = Appearance(self._data[Character.APPEARANCE])

        return self._appearance

    @property
    def talents(self):
        if self._refresh_if_not_present(Character.TALENTS):
            self._talents = [Build(self, build) for build in self._data[Character.TALENTS]]

        return self._talents

    @property
    def stats(self):
        if self._refresh_if_not_present(Character.STATS):
            self._stats = Stats(self._data[Character.STATS])

        return self._stats

    def refresh(self, *fields):
        for field in fields:
            self._fields.add(field)
            
        self.populate(self.connection.get_character(self.region, self._data['realm'],
            self.name, raw=True, fields=self._fields))

        for field in self._fields:
            try:
                delattr(self, '_' + field)
            except AttributeError:
                pass

    def get_realm_name(self):
        return normalize(self._data['realm'])

    def get_class_name(self):
        return CLASS.get(self.class_, 'Unknown')

    def get_spec_name(self):
        for talent in self.talents:
            if talent.selected:
                return talent.name

        return ''

    def get_full_class_name(self):
        spec_name = self.get_spec_name()
        class_name = self.get_class_name()

        return ('%s %s' % (spec_name, class_name)).strip()

    def get_race_name(self):
        return RACE.get(self.race, 'Unknown')

    def get_thumbnail_url(self):
        return 'http://%(region)s.battle.net/static-render/%(region)s/%(path)s' % {
            'region': self.region,
            'path': self.thumbnail
        }

class Title(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data
        
        self.id = data['id']
        self.format = data['name']

    def __str__(self):
        return self.format % self._character.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.format)

class Reputation(Thing):
    def __init__(self, data):
        self._data = data

        self.id = data['id']
        self.name = data['name']
        self.standing = data['standing']
        self.value = data['value']
        self.max = data['max']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    @property
    def percent(self):
        return int(100.0 * self.value / self.max)

class Guild(Thing):
    def __init__(self, region, realm=None, name=None, data=None, connection=None):
        self.region = region
        self.connection = connection or make_connection()

        if realm and name:
            pass # TODO: Add when Guild API exists!

        self._data = data

        self.name = normalize(data['name'])
        self.level = data['level']
        self.members = data['members']
        self.level = data['level']
        self.emblem = Emblem(data['emblem'])
        self.achievement_points = data['achievementPoints']

    def __len__(self):
        return self.members

    def __repr__(self):
        return '<%s: %s@%s>' % (self.__class__.__name__, self.name, self.realm)

    @property
    def roster(self):
        return []

    @property
    def realm(self):
        if not hasattr(self, '_realm'):
            self._realm = Realm(self.region, self._data['realm'], connection=self.connection)

        return self._realm

    def get_realm_name(self):
        return normalize(self._data['realm'])

class Realm(Thing):
    PVP = 'pvp'
    PVE = 'pve'
    RP = 'rp'
    RPPVP = 'rppvp'

    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

    def __init__(self, region, name=None, data=None, connection=None):
        self.region = region
        self.connection = connection or make_connection()

        if name and not data:
            data = self.connection.get_realm(region, name, raw=True)

        self.populate(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s(%s)>' % (self.__class__.__name__, self.name, self.region.upper())

    def populate(self, data):
        self._data = data

        self.name = normalize(data['name'])
        self.slug = data['slug']
        self.status = data['status']
        self.queue = data['queue']
        self.population = data['population']
        self.type = data['type']

    def refresh(self):
        self.populate(self.connection.get_realm(self.name))

    def has_queue(self):
        return self.queue

    def is_online(self):
        return self.status

    def is_offline(self):
        return not self.status

class Item(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data

        self.id = data['id']
        self.name = data['name']
        self.quality = data['quality']
        self.icon = data['icon']

        self.reforge = data['tooltipParams'].get('reforge')
        self.set = data['tooltipParams'].get('set')
        self.enchant = data['tooltipParams'].get('enchant')
        self.extra_socket = data['tooltipParams'].get('extraSocket', False)

        self.gems = collections.defaultdict(lambda: None)

        for key, value in data['tooltipParams'].items():
            if key.startswith('gem'):
                self.gems[int(key[3:])] = value

    def __str__(self):
        return self.name
                
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    def get_quality_name(self):
        return QUALITY.get(self.quality, 'Unknown')

    def get_icon_url(self, size='large'):
        return make_icon_url(self._character.region, self.icon, size)

class Stats(Thing):
    def __init__(self, data):
        self._data = data

        self.agility = data['agi']
        self.armor = data['armor']
        self.attack_power = data['attackPower']
        self.block = data['block']
        self.block_rating = data['blockRating']
        self.crit = data['crit']
        self.crit_rating = data['critRating']
        self.dodge = data['dodge']
        self.dodge_rating = data['dodgeRating']
        self.expertise_rating = data['expertiseRating']
        self.haste_rating = data['hasteRating']
        self.health = data['health']
        self.hit_rating = data['hitRating']
        self.intellect = data['int']
        self.main_hand_damage_max = data['mainHandDmgMax']
        self.main_hand_damage_min = data['mainHandDmgMin']
        self.main_hand_dps = data['mainHandDps']
        self.main_hand_expertise = data['mainHandExpertise']
        self.main_hand_speed = data['mainHandSpeed']
        self.mana_regen = data['mana5']
        self.mana_regen_combat = data['mana5Combat']
        self.mastery = data['mastery']
        self.mastery_rating = data['masteryRating']
        self.off_hand_damage_max = data['offHandDmgMax']
        self.off_hand_damage_min = data['offHandDmgMin']
        self.off_hand_dps = data['offHandDps']
        self.off_hand_expertise = data['offHandExpertise']
        self.off_hand_speed = data['offHandSpeed']
        self.parry = data['parry']
        self.parry_rating = data['parryRating']
        self.power = data['power']
        self.power_type = data['powerType']
        self.ranged_attack_power = data['rangedAttackPower']
        self.ranged_crit = data['rangedCrit']
        self.ranged_crit_rating = data['rangedCritRating']
        self.ranged_damage_max = data['rangedDmgMax']
        self.ranged_damage_min = data['rangedDmgMin']
        self.ranged_dps = data['rangedDps']
        self.ranged_hit_rating = data['rangedHitRating']
        self.ranged_speed = data['rangedSpeed']
        self.resilience = data['resil']
        self.spell_crit = data['spellCrit']
        self.spell_crit_rating = data['spellCritRating']
        self.spell_penetration = data['spellPen']
        self.spell_power = data['spellPower']
        self.spirit = data['spr']
        self.stamina = data['sta']
        self.strength = data['str']

class Appearance(Thing):
    def __init__(self, data):
        self._data = data
        
        self.face = data['faceVariation']
        self.feature = data['featureVariation']
        self.hair = data['hairVariation']
        self.hair_color = data['hairColor']
        self.show_cloak = data['showCloak']
        self.show_helm = data['showHelm']
        self.skin_color = data['skinColor']

class Emblem(Thing):
    def __init__(self, data):
        self._data = data

        self.border = data['border']
        self.border_color = data['borderColor']
        self.icon = data['icon']
        self.icon_color = data['iconColor']
        self.background_color = data['backgroundColor']

class Equipment(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data

        self.average_item_level = data['averageItemLevel']
        self.average_item_level_equiped = data['averageItemLevelEquipped']

        self.main_hand = Item(self._character, data['mainHand']) if data.get('mainHand') else None
        self.off_hand = Item(self._character, data['offHand']) if data.get('offHand') else None
        self.ranged = Item(self._character, data['ranged']) if data.get('ranged') else None

        self.head = Item(self._character, data['head']) if data.get('head') else None
        self.neck = Item(self._character, data['neck']) if data.get('neck') else None
        self.shoulder = Item(self._character, data['shoulder']) if data.get('shoulder') else None
        self.back = Item(self._character, data['back']) if data.get('back') else None
        self.chest = Item(self._character, data['chest']) if data.get('chest') else None
        self.shirt = Item(self._character, data['shirt']) if data.get('shirt') else None
        self.tabard = Item(self._character, data['tabard']) if data.get('tabard') else None
        self.wrist = Item(self._character, data['wrist']) if data.get('wrist') else None

        self.hands = Item(self._character, data['hands']) if data.get('hands') else None
        self.waist = Item(self._character, data['waist']) if data.get('waist') else None
        self.legs = Item(self._character, data['legs']) if data.get('legs') else None
        self.feet = Item(self._character, data['feet']) if data.get('feet') else None
        self.finger1 = Item(self._character, data['finger1']) if data.get('finger1') else None
        self.finger2 = Item(self._character, data['finger2']) if data.get('finger2') else None
        self.trinket1 = Item(self._character, data['trinket1']) if data.get('trinket1') else None
        self.trinket2 = Item(self._character, data['trinket2']) if data.get('trinket2') else None

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise IndexError

class Build(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data

        self.build = data['build']
        self.icon = data['icon']
        self.name = data['name']
        self.selected = data.get('selected', False)
        self.glyphs = {}

        for type_ in ['prime', 'major', 'minor']:
            self.glyphs[type_] = [Glyph(self, glyph) for glyph in data['glyphs'][type_]]

        Tree = collections.namedtuple('Tree', ('points', 'total',))
        self.trees = [Tree(**tree) for tree in data['trees']]

    def __str__(self):
        return self.name + ' (%d/%d/%d' % tuple(map(operator.attrgetter('total'), self.trees))

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def get_icon_url(self, size='large'):
        return make_icon_url(self._character.region, self.icon, size)

class Glyph(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data

        self.name = data['name']
        self.glyph = data['glyph']
        self.item = data['item']
        self.icon = data['icon']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    def get_icon_url(self, size='large'):
        return make_icon_url(self._character.region, self.icon, size)

class Profession(Thing):
    def __init__(self, character, data):
        self._character = character
        self._data = data

        self.id = data['id']
        self.name = data['name']
        self.max = data['max']
        self.rank = data['rank']
        self.icon = data['icon']
        self.recipes = data['recipes']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

class Pet(Thing):
    def __init__(self, data):
        self._data = data

        self.name = data['name']
        self.creature = data['creature']
        self.slot = data['slot']

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)
