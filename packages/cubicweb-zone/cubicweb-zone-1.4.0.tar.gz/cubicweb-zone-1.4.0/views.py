"""Specific ui views for the Zone entity type

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"
_ = unicode

from logilab.common.decorators import monkeypatch

from cubicweb.selectors import is_instance
from cubicweb.web import uicfg, facet, box
from cubicweb.web.views import basecontrollers

_abaa = uicfg.actionbox_appearsin_addmenu
_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl

_abaa.tag_object_of(('Zone', 'situated_in', 'Zone'), True)
_pvs.tag_subject_of(('*', 'situated_in', '*'), 'hidden')
_pvdc.tag_attribute(('Zone', 'description'), {'showlabel': False})


class SituatedInFacet(facet.RelationFacet):
    __regid__ = 'situated_in-facet'
    rtype = 'situated_in'
    target_attr = 'name'
    label_vid = 'combobox'





class ZoneBox(box.AjaxEditRelationBoxTemplate):
    __regid__ = 'zone.zone-box'

    rtype = 'situated_in'
    role = 'subject'
    target_etype = 'Zone'

    order = 0

    added_msg = _('zone has been updated')
    removed_msg = _('zone has been removed')

    fname_vocabulary = 'unrelated_zones'
    fname_validate = 'link_to_zone'
    fname_remove = 'unlink_zone'


@monkeypatch(basecontrollers.JSonController)
@basecontrollers.jsonize
def js_unrelated_zones(self, eid):
    """return tag unrelated to an entity"""
    rset = self._cw.execute('Any Z, ZN WHERE Z name ZN, NOT X situated_in Z, X eid %(x)s',
                            {'x' : eid})
    return [z.view('combobox') for z in rset.entities()]


@monkeypatch(basecontrollers.JSonController)
def js_link_to_zone(self, eid, value):
    req = self._cw
    zone = None
    for part in value.split('>'):
        partname = part.strip().title()
        if not partname:
            continue
        rset = req.execute('Zone Z WHERE Z name %(name)s', {'name': partname})
        if rset:
            partzone = rset.get_entity(0, 0)
        elif zone is None:
            partzone = req.create_entity('Zone', name=partname)
        else:
            partzone = req.create_entity('Zone', name=partname, situated_in=zone)
        zone = partzone
    if zone is not None:
        req.execute('SET X situated_in Z WHERE '
                    'Z eid %(z)s, X eid %(x)s, NOT X situated_in Z',
                    {'z': zone.eid, 'x' : eid})

@monkeypatch(basecontrollers.JSonController)
def js_unlink_zone(self, eid, zoneeid):
    self._cw.execute('DELETE X situated_in Z WHERE Z eid %(z)s, X eid %(x)s',
                     {'z': zoneeid, 'x': eid})
