# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
from urllib2 import URLError, HTTPError
'''
Created on May 10, 2011

@author: evan
'''

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError
from lxml import etree
import base64



__all__ = [
    'Ticket',
    'TicketAttachment',
    'TicketNote',
    'TicketPost',
    'TicketPriority',
    'TicketStatus',
    'TicketType',
]

class Ticket(KayakoObject):
    '''
    Kayako Ticket API Object.
    
    subject          The Ticket Subject
    fullname         Full Name of creator
    email            Email Address of creator
    contents         The contents of the first ticket post
    departmentid     The Department ID
    ticketstatusid   The Ticket Status ID
    ticketpriorityid The Ticket Priority ID
    tickettypeid     The Ticket Type ID
    userid           The User ID, if the ticket is to be created as a user.
    staffid          The Staff ID, if the ticket is to be created as a staff
    ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
    type             The ticket type: 'default' or 'phone' 
    '''

    controller = '/Tickets/Ticket'

    __parameters__ = [
        'id',
        'subject',
        'fullname',
        'email',
        'contents',
        'departmentid',
        'ticketstatusid',
        'ticketpriorityid', # synonym for priorityid
        'tickettypeid',
        'userid',
        'staffid',
        'ownerstaffid',
        'type',
        'flagtype',
        'displayid',
        'statusid',
        'typeid',
        'userorganization',
        'userorganizationid',
        'ownerstaffname',
        'lastreplier',
        'creationtime',
        'lastactivity',
        'laststaffreply',
        'lastuserreply',
        'slaplanid',
        'nextreplydue',
        'resolutiondue',
        'replies',
        'ipaddress',
        'creator',
        'creationmode',
        'creationtype',
        'isescalated',
        'escalationruleid',
        'tags',
        'watchers',
        'workflows',
        'notes',
        'posts',
    ]

    __required_add_parameters__ = ['subject', 'fullname', 'email', 'contents', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'tickettypeid', ]
    __add_parameters__ = ['subject', 'fullname', 'email', 'contents', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'tickettypeid', 'userid', 'staffid', 'ownerstaffid', 'type']

    __required_save_parameters__ = []
    __save_parameters__ = ['subject', 'fullname', 'email', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'ownerstaffid', 'userid', ]

    @classmethod
    def _parse_ticket(cls, api, ticket_tree):

        ticketid = cls._parse_int(ticket_tree.get('id'))

        workflows = [dict(id=workflow_node.get('id'), title=workflow_node.get('title')) for workflow_node in ticket_tree.findall('workflow')]
        watchers = [dict(staffid=watcher_node.get('staffid'), name=watcher_node.get('name')) for watcher_node in ticket_tree.findall('watcher')]
        notes = [TicketNote(api, **TicketNote._parse_ticket_note(ticket_note_tree, ticketid)) for ticket_note_tree in ticket_tree.findall('note')]

        posts = []
        posts_node = ticket_tree.find('posts')
        if posts_node is not None:
            posts = [TicketPost(api, **TicketPost._parse_ticket_post(ticket_post_tree, ticketid)) for ticket_post_tree in posts_node.findall('post')]

        params = dict(
            id=ticketid,
            subject=cls._get_string(ticket_tree.find('subject')),
            fullname=cls._get_string(ticket_tree.find('fullname')),
            email=cls._get_string(ticket_tree.find('email')),
            departmentid=cls._get_int(ticket_tree.find('departmentid')),
            ticketstatusid=cls._get_int(ticket_tree.find('ticketstatusid'), required=False),
            ticketpriorityid=cls._get_int(ticket_tree.find('priorityid')), # Note the difference, request param is ticketpriorityid, response is priorityid
            tickettypeid=cls._get_int(ticket_tree.find('tickettypeid'), required=False),
            userid=cls._get_int(ticket_tree.find('userid')),
            ownerstaffid=cls._get_int(ticket_tree.find('ownerstaffid')),
            flagtype=cls._parse_int(ticket_tree.get('flagtype'), 'flagtype'),
            displayid=cls._get_string(ticket_tree.find('displayid')),
            statusid=cls._get_int(ticket_tree.find('statusid')),
            typeid=cls._get_int(ticket_tree.find('typeid')),
            userorganization=cls._get_string(ticket_tree.find('userorganization')),
            userorganizationid=cls._get_int(ticket_tree.find('userorganizationid'), required=False),
            ownerstaffname=cls._get_string(ticket_tree.find('ownerstaffname')),
            lastreplier=cls._get_string(ticket_tree.find('lastreplier')),
            creationtime=cls._get_date(ticket_tree.find('creationtime')),
            lastactivity=cls._get_date(ticket_tree.find('lastactivity')),
            laststaffreply=cls._get_date(ticket_tree.find('laststaffreply')),
            lastuserreply=cls._get_date(ticket_tree.find('lastuserreply')),
            slaplanid=cls._get_int(ticket_tree.find('slaplanid')),
            nextreplydue=cls._get_date(ticket_tree.find('nextreplydue')),
            resolutiondue=cls._get_date(ticket_tree.find('resolutiondue')),
            replies=cls._get_int(ticket_tree.find('replies')),
            ipaddress=cls._get_string(ticket_tree.find('ipaddress')),
            creator=cls._get_int(ticket_tree.find('creator')),
            creationmode=cls._get_int(ticket_tree.find('creationmode')),
            creationtype=cls._get_int(ticket_tree.find('creationtype')),
            isescalated=cls._get_boolean(ticket_tree.find('isescalated')),
            escalationruleid=cls._get_int(ticket_tree.find('escalationruleid')),
            tags=cls._get_string(ticket_tree.find('tags')),
            watchers=watchers,
            workflows=workflows,
            notes=notes,
            posts=posts,
        )
        return params

    def _update_from_response(self, ticket_tree):

        ticketid = self._parse_int(ticket_tree.get('id'))
        if ticketid is not None:
            self.id = ticketid

        priority_node = ticket_tree.find('priorityid')
        if priority_node is not None:
            self.ticketpriorityid = self._get_int(priority_node)

        for int_node in ['departmentid', 'userid', 'ownerstaffid', 'flagtype', 'statusid', 'slaplanid', 'replies', 'creator', 'creationmode', 'creationtype', 'escalationruleid', 'ticketstatusid', 'tickettypeid', 'userorganizationid' ]:
            node = ticket_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['subject', 'email', 'displayid', 'userorganization', 'ownerstaffname', 'lastreplier', 'ipaddress', 'tags']:
            node = ticket_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for bool_node in ['isescalated']:
            node = ticket_tree.find(bool_node)
            if node is not None:
                setattr(self, bool_node, self._get_boolean(node, required=False))

        for date_node in ['creationtime', 'lastactivity', 'lastuserreply', 'nextreplydue', 'resolutiondue', ]:
            node = ticket_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, departmentid, ticketstatusid= -1, ownerstaffid= -1, userid= -1):
        '''
        Get all of the tickets filtered by the parameters:
        Lists are converted to comma-separated values.
        Required:
            departmentid     Filter the tickets by the specified department id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
        Optional:
            ticketstatusid   Filter the tickets by the specified ticket status id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
            ownerstaffid     Filter the tickets by the specified owner staff id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
            userid           Filter the tickets by the specified user id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3 
        '''

        if isinstance(departmentid, (list, tuple)):
            departmentid = ','.join([str(id_item) for id_item in departmentid])
        if isinstance(ticketstatusid, (list, tuple)):
            ticketstatusid = ','.join([str(id_item) for id_item in ticketstatusid])
        if isinstance(ownerstaffid, (list, tuple)):
            ownerstaffid = ','.join([str(id_item) for id_item in ownerstaffid])
        if isinstance(userid, (list, tuple)):
            userid = ','.join([str(id_item) for id_item in userid])

        response = api._request('%s/ListAll/%s/%s/%s/%s/' % (cls.controller, departmentid, ticketstatusid, ownerstaffid, userid), 'GET')
        tree = etree.parse(response)
        return [Ticket(api, **cls._parse_ticket(api, ticket_tree)) for ticket_tree in tree.findall('ticket')]

    @classmethod
    def get(cls, api, id):
        try:
            response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        except KayakoResponseError, error:
            if len(error.args) and isinstance(error.args[0], (URLError, HTTPError)) and error.args[0].getcode() == 404:
                return None
        tree = etree.parse(response)
        node = tree.find('ticket')
        if node is None:
            return None
        params = cls._parse_ticket(api, node)
        return Ticket(api, **params)

    def add(self):
        '''
        Add this Ticket.
        
        Requires:
            subject          The Ticket Subject
            fullname         Full Name of creator
            email            Email Address of creator
            contents         The contents of the first ticket post
            departmentid     The Department ID
            ticketstatusid   The Ticket Status ID
            ticketpriorityid The Ticket Priority ID
            tickettypeid     The Ticket Type ID
        At least one of these must be present:
            userid           The User ID, if the ticket is to be created as a user.
            staffid          The Staff ID, if the ticket is to be created as a staff
        Optional:
            ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
            type             The ticket type: 'default' or 'phone'
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters
        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if 'userid' not in parameters and 'staffid' not in parameters:
            raise KayakoRequestError('To add a Ticket, at least one of the following parameters must be set: userid, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('ticket')
        self._update_from_response(node)

    def save(self):
        '''
        Save this ticket.
        
        Saves only the following:
            subject          The Ticket Subject
            fullname         Full Name of creator
            email            Email Address of creator
            departmentid     The Department ID
            ticketstatusid   The Ticket Status ID
            ticketpriorityid The Ticket Priority ID
            tickettypeid     The Ticket Type ID
            ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
            userid           The User ID, if you want to change the user for this ticket 
        '''
        response = self._save('%s/%s/' % (self.controller, self.id))
        tree = etree.parse(response)
        node = tree.find('ticket')
        self._update_from_response(node)

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<Ticket (%s): %s>' % (self.id, self.subject)

class TicketAttachment(KayakoObject):
    '''
    Kayako TicketAttachment API Object.
    
    ticketid     The unique numeric identifier of the ticket.
    ticketpostid The unique numeric identifier of the ticket post.
    filename     The file name for the attachment
    contents     The BASE64 encoded attachment contents 
    filesize
    filetype
    dateline
    '''

    controller = '/Tickets/TicketAttachment'

    __parameters__ = [
        'id',
        'ticketid',
        'ticketpostid',
        'filename',
        'filesize',
        'filetype',
        'contents',
        'dateline',
    ]

    __required_add_parameters__ = ['ticketid', 'ticketpostid', 'filename', 'contents']
    __add_parameters__ = ['ticketid', 'ticketpostid', 'filename', 'contents']

    __required_save_parameters__ = []
    ''' Save not available for TicketAttachment. '''
    __save_parameters__ = []
    ''' Save not available for TicketAttachment. '''


    @classmethod
    def _parse_ticket_attachment(cls, ticket_attachment_tree):

        params = dict(
            id=cls._get_int(ticket_attachment_tree.find('id')),
            ticketid=cls._get_int(ticket_attachment_tree.find('ticketid')),
            ticketpostid=cls._get_int(ticket_attachment_tree.find('ticketpostid')),
            filename=cls._get_string(ticket_attachment_tree.find('filename')),
            filesize=cls._get_int(ticket_attachment_tree.find('filesize')),
            filetype=cls._get_string(ticket_attachment_tree.find('filetype')),
            contents=cls._get_string(ticket_attachment_tree.find('contents')),
            dateline=cls._get_date(ticket_attachment_tree.find('dateline')),
        )
        return params

    def _update_from_response(self, ticket_attachment_tree):
        for int_node in ['id', 'ticketid', 'ticketpostid', 'filesize']:
            node = ticket_attachment_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['filename', 'filetype', 'contents']:
            node = ticket_attachment_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for date_node in ['dateline']:
            node = ticket_attachment_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketAttachments for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketAttachment(api, **cls._parse_ticket_attachment(ticket_attachment_tree)) for ticket_attachment_tree in tree.findall('attachment')]

    @classmethod
    def get(cls, api, ticketid, attachmentid):
        try:
            response = api._request('%s/%s/%s/' % (cls.controller, ticketid, attachmentid), 'GET')
        except KayakoResponseError, error:
            if len(error.args) and isinstance(error.args[0], (URLError, HTTPError)) and error.args[0].getcode() == 404:
                return None
        tree = etree.parse(response)
        node = tree.find('attachment')
        if node is None:
            return None
        params = cls._parse_ticket_attachment(node)
        return TicketAttachment(api, **params)

    def add(self):
        '''
        Add this TicketAttachment.
        
        Requires:
            ticketid     The unique numeric identifier of the ticket.
            ticketpostid The unique numeric identifier of the ticket post.
            filename     The file name for the attachment
            contents     The BASE64 encoded attachment contents 
        '''
        response = self._add(self.controller)
        tree = etree.parse(response)
        node = tree.find('attachment')
        self._update_from_response(node)

    def delete(self):
        if self.ticketid is None or self.ticketid is UnsetParameter:
            raise KayakoRequestError('Cannot delete a TicketAttachment without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def get_contents(self):
        ''' Return the unencoded contents of this TicketAttachment. '''
        if self.contents:
            return base64.b64decode(self.contents)

    def set_contents(self, contents):
        ''' 
        Set this TicketAttachment's contents to Base 64 encoded data, or set the
        contents to nothing.
        '''
        if contents:
            self.contents = base64.b64encode(contents)
        else:
            self.contents = None

    def __str__(self):
        return '<TicketAttachment (%s): %s>' % (self.id, self.filename)

class TicketNote(KayakoObject):
    '''
    Kayako TicketNote API Object.
    
    ticketid     The unique numeric identifier of the ticket.
    contents     The ticket note contents
    staffid      The Staff ID, if the ticket is to be created as a staff.
    fullname     The Fullname, if the ticket is to be created without providing a staff user. Example: System messages, Alerts etc.
    forstaffid   The Staff ID, this value can be provided if you wish to restrict the note visibility to a specific staff
    notecolor    The Note Color, for more information see note colors (http://wiki.kayako.com/display/DEV/Mobile+-+Constants)
    '''

    controller = '/Tickets/TicketNote'

    __parameters__ = [
        'id',
        'ticketid',
        'contents',
        'staffid',
        'fullname',
        'forstaffid',
        'notecolor',
        'type',
        'creatorstaffid',
        'creatorstaffname',
        'creationdate',
    ]

    __required_add_parameters__ = ['ticketid', 'contents']
    __add_parameters__ = ['ticketid', 'contents', 'staffid', 'fullname', 'forstaffid', 'notecolor']

    __required_save_parameters__ = []
    ''' Save not available for TicketNote. '''
    __save_parameters__ = []
    ''' Save not available for TicketNote. '''

    @classmethod
    def _parse_ticket_note(cls, ticket_note_tree, ticketid):
        params = dict(
            ticketid=ticketid,
            contents=ticket_note_tree.text,
            staffid=cls._parse_int(ticket_note_tree.get('staffid'), required=False),
            forstaffid=cls._parse_int(ticket_note_tree.get('forstaffid')),
            notecolor=cls._parse_int(ticket_note_tree.get('notecolor')),
            type=ticket_note_tree.get('type'),
            creatorstaffid=cls._parse_int(ticket_note_tree.get('creatorstaffid')),
            creatorstaffname=ticket_note_tree.get('creatorstaffname'),
            creationdate=cls._parse_date(ticket_note_tree.get('creationdate')),
        )
        return params

    def _update_from_response(self, ticket_note_tree):

        self.contents = ticket_note_tree.text

        for int_attr in ['staffid', 'forstaffid', 'notecolor', 'creatorstaffid']:
            attr = ticket_note_tree.get(int_attr)
            if attr is not None:
                setattr(self, int_attr, self._parse_int(attr, required=False))

        for str_attr in ['type', 'creatorstaffname']:
            attr = ticket_note_tree.get(str_attr)
            if attr is not None:
                setattr(self, str_attr, attr)

        for date_attr in ['creationdate']:
            attr = ticket_note_tree.get(date_attr)
            if attr is not None:
                setattr(self, date_attr, self._parse_date(attr, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketNotes for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketNote(api, **cls._parse_ticket_note(ticket_note_tree, ticketid)) for ticket_note_tree in tree.findall('note')]

#    @classmethod
#    def get(cls, api, ticketid, id):
#        response = api._request('%s/%s/%s/' % (cls.controller, ticketid, id), 'GET')
#        tree = etree.parse(response)
#        node = tree.find('note')
#        if node is None:
#            return None
#        params = cls._parse_ticket_note(node, ticketid)
#        return TicketNote(api, **params)

    def add(self):
        '''
        Add this TicketNote.
        
        Requires:
            ticketid     The unique numeric identifier of the ticket.
            contents     The ticket note contents
        Requires one:
            staffid      The Staff ID, if the ticket is to be created as a staff.
            fullname     The Fullname, if the ticket is to be created without providing a staff user. Example: System messages, Alerts etc.
        Optional:
            forstaffid   The Staff ID, this value can be provided if you wish to restrict the note visibility to a specific staff
            notecolor    The Note Color, for more information see note colors
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters

        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if ('fullname' not in parameters and 'staffid' not in parameters) or ('fullname' in parameters and 'staffid' in parameters):
            raise KayakoRequestError('To add a TicketNote, just one of the following parameters must be set: fullname, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('note')
        self._update_from_response(node)

#    def delete(self):
#        if self.ticketid is None or self.ticketid is UnsetParameter:
#            raise KayakoRequestError('Cannot delete a TicketNote without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
#        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def __str__(self):
        return '<TicketNote (%s): %s>' % (self.id, self.contents[:20])

class TicketPost(KayakoObject):
    '''
    Kayako TicketPost API Object.
    
    ticketid   The unique numeric identifier of the ticket.
    subject    The ticket post subject
    contents   The ticket post contents
    userid     The User ID, if the ticket post is to be created as a user.
    staffid    The Staff ID, if the ticket post is to be created as a staff
    dateline
    fullname
    email
    emailto
    ipaddress
    hasattachments
    creator
    isthirdparty
    ishtml
    isemailed
    issurveycomment
    '''

    __parameters__ = [
        'id',
        'ticketid',
        'subject',
        'contents',
        'userid',
        'staffid',
        'dateline',
        'fullname',
        'email',
        'emailto',
        'ipaddress',
        'hasattachments',
        'creator',
        'isthirdparty',
        'ishtml',
        'isemailed',
        'issurveycomment',
    ]

    __required_add_parameters__ = ['ticketid', 'subject', 'contents']
    __add_parameters__ = ['ticketid', 'subject', 'contents', 'userid', 'staffid']

    __required_save_parameters__ = []
    ''' Save not available for TicketNote. '''
    __save_parameters__ = []
    ''' Save not available for TicketNote. '''

    controller = '/Tickets/TicketPost'

    @classmethod
    def _parse_ticket_post(cls, ticket_post_tree, ticket_id):

        params = dict(
            id=cls._get_int(ticket_post_tree.find('ticketpostid')), # Note different names
            ticketid=ticket_id,
            subject=cls._get_string(ticket_post_tree.find('subject')),
            contents=cls._get_string(ticket_post_tree.find('contents')),
            userid=cls._get_int(ticket_post_tree.find('userid')),
            staffid=cls._get_int(ticket_post_tree.find('staffid')),
            dateline=cls._get_date(ticket_post_tree.find('dateline')),
            fullname=cls._get_string(ticket_post_tree.find('fullname')),
            email=cls._get_string(ticket_post_tree.find('email')),
            emailto=cls._get_string(ticket_post_tree.find('emailto')),
            ipaddress=cls._get_string(ticket_post_tree.find('ipaddress')),
            hasattachments=cls._get_boolean(ticket_post_tree.find('hasattachments')),
            creator=cls._get_int(ticket_post_tree.find('creator')),
            isthirdparty=cls._get_boolean(ticket_post_tree.find('isthirdparty')),
            ishtml=cls._get_boolean(ticket_post_tree.find('ishtml')),
            isemailed=cls._get_boolean(ticket_post_tree.find('isemailed')),
            issurveycomment=cls._get_boolean(ticket_post_tree.find('issurveycomment')),
        )
        return params

    def _update_from_response(self, ticket_post_tree):

        ticketpostid_node = ticket_post_tree.find('ticketpostid')
        if ticketpostid_node is not None:
            self.id = self._get_int(ticketpostid_node)

        for int_node in ['userid', 'staffid', 'creator']:
            node = ticket_post_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['subject', 'contents', 'fullname', 'email', 'emailto', 'ipaddress']:
            node = ticket_post_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for bool_node in ['hasattachments', 'isthirdparty', 'ishtml', 'isemailed', 'issurveycomment']:
            node = ticket_post_tree.find(bool_node)
            if node is not None:
                setattr(self, bool_node, self._get_boolean(node, required=False))

        for date_node in ['dateline']:
            node = ticket_post_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketPosts for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketPost(api, **cls._parse_ticket_post(ticket_post_tree, ticketid)) for ticket_post_tree in tree.findall('post')]

    @classmethod
    def get(cls, api, ticketid, id):
        try:
            response = api._request('%s/%s/%s/' % (cls.controller, ticketid, id), 'GET')
        except KayakoResponseError, error:
            if len(error.args) and isinstance(error.args[0], (URLError, HTTPError)) and error.args[0].getcode() == 404:
                return None
        tree = etree.parse(response)
        node = tree.find('post')
        if node is None:
            return None
        params = cls._parse_ticket_post(node, ticketid)
        return TicketPost(api, **params)

    def add(self):
        '''
        Add this TicketPost.
        
        Requires:
            ticketid  The unique numeric identifier of the ticket.
            subject   The ticket post subject
            contents  The ticket post contents
        Requires one of:
            userid    The User ID, if the ticket post is to be created as a user.
            staffid   The Staff ID, if the ticket post is to be created as a staff 
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters

        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if ('userid' not in parameters and 'staffid' not in parameters) or ('userid' in parameters and 'staffid' in parameters):
            raise KayakoRequestError('To add a TicketPost, just one of the following parameters must be set: userid, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('post')
        self._update_from_response(node)

    def delete(self):
        if self.ticketid is None or self.ticketid is UnsetParameter:
            raise KayakoRequestError('Cannot delete a TicketPost without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def __str__(self):
        return '<TicketPost (%s): %s>' % (self.id, self.subject)

class TicketPriority(KayakoObject):
    '''
    Kayako TicketPriority API Object.
    
    id
    title
    displayorder
    frcolorcode
    bgcolorcode
    displayicon
    type
    uservisibilitycustom
    usergroupid

    '''

    controller = '/Tickets/TicketPriority'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'frcolorcode',
        'bgcolorcode',
        'displayicon',
        'type',
        'uservisibilitycustom',
        'usergroupid',
    ]

    __required_add_parameters__ = []
    ''' Add not available for TicketPriority. '''
    __add_parameters__ = []
    ''' Add not available for TicketPriority. '''

    __required_save_parameters__ = []
    ''' Save not available for TicketPriority. '''
    __save_parameters__ = []
    ''' Save not available for TicketPriority. '''

    @classmethod
    def _parse_ticket_priority(cls, ticket_priority_tree):

        params = dict(
            id=cls._get_int(ticket_priority_tree.find('id')),
            title=cls._get_string(ticket_priority_tree.find('title')),
            displayorder=cls._get_int(ticket_priority_tree.find('displayorder')),
            frcolorcode=cls._get_string(ticket_priority_tree.find('frcolorcode')),
            bgcolorcode=cls._get_string(ticket_priority_tree.find('bgcolorcode')),
            displayicon=cls._get_string(ticket_priority_tree.find('displayicon')),
            type=cls._get_string(ticket_priority_tree.find('type')),
            uservisibilitycustom=cls._get_boolean(ticket_priority_tree.find('uservisibilitycustom')),
            usergroupid=cls._get_int(ticket_priority_tree.find('usergroupid'), required=False),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketPriority(api, **cls._parse_ticket_priority(ticket_priority_tree)) for ticket_priority_tree in tree.findall('ticketpriority')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('ticketpriority')
        if node is None:
            return None
        params = cls._parse_ticket_priority(tree.find('ticketpriority'))
        return TicketPriority(api, **params)

    def __str__(self):
        return '<TicketPriority (%s): %s>' % (self.id, self.title)

class TicketStatus(KayakoObject):
    '''
    Kayako TicketStatus API Object.
    
    id
    title
    displayorder
    departmentid
    displayicon
    type
    displayinmainlist
    markasresolved
    displaycount
    statuscolor
    statusbgcolor
    resetduetime
    triggersurvey
    staffvisibilitycustom

    '''

    controller = '/Tickets/TicketStatus'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'departmentid',
        'displayicon',
        'type',
        'displayinmainlist',
        'markasresolved',
        'displaycount',
        'statuscolor',
        'statusbgcolor',
        'resetduetime',
        'triggersurvey',
        'staffvisibilitycustom',
    ]

    __required_add_parameters__ = []
    ''' Add not available for TicketStatus. '''
    __add_parameters__ = []
    ''' Add not available for TicketStatus. '''

    __required_save_parameters__ = []
    ''' Save not available for TicketStatus. '''
    __save_parameters__ = []
    ''' Save not available for TicketStatus. '''

    @classmethod
    def _parse_ticket_status(cls, ticket_status_tree):

        params = dict(
            id=cls._get_int(ticket_status_tree.find('id')),
            title=cls._get_string(ticket_status_tree.find('title')),
            displayorder=cls._get_int(ticket_status_tree.find('displayorder')),
            departmentid=cls._get_int(ticket_status_tree.find('departmentid')),
            displayicon=cls._get_string(ticket_status_tree.find('displayicon')),
            type=cls._get_string(ticket_status_tree.find('type')),
            displayinmainlist=cls._get_boolean(ticket_status_tree.find('displayinmainlist')),
            markasresolved=cls._get_boolean(ticket_status_tree.find('markasresolved')),
            displaycount=cls._get_int(ticket_status_tree.find('displaycount')),
            statuscolor=cls._get_string(ticket_status_tree.find('statuscolor')),
            statusbgcolor=cls._get_string(ticket_status_tree.find('statusbgcolor')),
            resetduetime=cls._get_boolean(ticket_status_tree.find('resetduetime')),
            triggersurvey=cls._get_boolean(ticket_status_tree.find('triggersurvey')),
            staffvisibilitycustom=cls._get_boolean(ticket_status_tree.find('staffvisibilitycustom')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketStatus(api, **cls._parse_ticket_status(ticket_status_tree)) for ticket_status_tree in tree.findall('ticketstatus')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('ticketstatus')
        if node is None:
            return None
        params = cls._parse_ticket_status(node)
        return TicketStatus(api, **params)

    def __str__(self):
        return '<TicketStatus (%s): %s>' % (self.id, self.title)

class TicketType(KayakoObject):
    '''
    Kayako TicketType API Object.
    
    id
    title
    displayorder
    departmentid
    displayicon
    type
    uservisibilitycustom

    '''

    controller = '/Tickets/TicketType'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'departmentid',
        'displayicon',
        'type',
        'uservisibilitycustom',
    ]

    __required_add_parameters__ = []
    ''' Add not available for TicketType. '''
    __add_parameters__ = []
    ''' Add not available for TicketType. '''

    __required_save_parameters__ = []
    ''' Save not available for TicketType. '''
    __save_parameters__ = []
    ''' Save not available for TicketType. '''

    @classmethod
    def _parse_ticket_type(cls, ticket_type_tree):

        params = dict(
            id=cls._get_int(ticket_type_tree.find('id')),
            title=cls._get_string(ticket_type_tree.find('title')),
            displayorder=cls._get_int(ticket_type_tree.find('displayorder')),
            departmentid=cls._get_int(ticket_type_tree.find('departmentid')),
            displayicon=cls._get_string(ticket_type_tree.find('displayicon')),
            type=cls._get_string(ticket_type_tree.find('type')),
            uservisibilitycustom=cls._get_boolean(ticket_type_tree.find('uservisibilitycustom')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketType(api, **cls._parse_ticket_type(ticket_type_tree)) for ticket_type_tree in tree.findall('tickettype')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('tickettype')
        if node is None:
            return None
        params = cls._parse_ticket_type(node)
        return TicketType(api, **params)

    def __str__(self):
        return '<TicketType (%s): %s>' % (self.id, self.title)

