# python imports
import os

# django imports
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.contrib.webdesign.lorem_ipsum import paragraph, sentence, words

# lfc imports
from lfc.models import Portal
from lfc.models import Page
from lfc.models import WorkflowStatesInformation

# portlets import
from portlets.models import Slot

# workflows import
import workflows.utils
from workflows.models import State
from workflows.models import StateInheritanceBlock
from workflows.models import StatePermissionRelation
from workflows.models import Transition
from workflows.models import Workflow
from workflows.models import WorkflowPermissionRelation

# permissions imports
import permissions.utils

def load_data():

    site = Site.objects.all()[0]
    site.name = site.domain = "www.example.com"
    site.save()

    portal = Portal.objects.create()

    # Register roles
    anonymous     = permissions.utils.register_role("Anonymous")
    owner         = permissions.utils.register_role("Owner")
    editor        = permissions.utils.register_role("Editor")
    reader        = permissions.utils.register_role("Reader")
    reviewer      = permissions.utils.register_role("Reviewer")
    manager       = permissions.utils.register_role("Manager")

    # Registers permissions
    add    = permissions.utils.register_permission("Add", "add")
    delete = permissions.utils.register_permission("Delete", "delete")
    edit   = permissions.utils.register_permission("Edit", "edit")
    view   = permissions.utils.register_permission("View", "view")

    ctype = ContentType.objects.get_for_model(Portal)
    manage_portal = permissions.utils.register_permission("Manage Portal", "manage_portal", [ctype])

    # Create slots
    left_slot, created = Slot.objects.get_or_create(name="Left")
    right_slot, created = Slot.objects.get_or_create(name="Right")

    # Set permissions for portal
    permissions.utils.grant_permission(portal, anonymous, "view")

    permissions.utils.grant_permission(portal, editor, "add", )
    permissions.utils.grant_permission(portal, editor, "delete")
    permissions.utils.grant_permission(portal, editor, "view")
    permissions.utils.grant_permission(portal, editor, "edit")

    permissions.utils.grant_permission(portal, manager, "add", )
    permissions.utils.grant_permission(portal, manager, "delete")
    permissions.utils.grant_permission(portal, manager, "edit")
    permissions.utils.grant_permission(portal, manager, "manage_portal")
    permissions.utils.grant_permission(portal, manager, "view")

    permissions.utils.grant_permission(portal, owner, "add")
    permissions.utils.grant_permission(portal, owner, "delete")
    permissions.utils.grant_permission(portal, owner, "edit")
    permissions.utils.grant_permission(portal, owner, "view")

    permissions.utils.grant_permission(portal, reader, "view")
    permissions.utils.grant_permission(portal, reviewer, "view")

    # Simple Workflow
    ##########################################################################

    # Add workflow
    workflow, created = Workflow.objects.get_or_create(name="Simple")

    # Add states
    private = State.objects.create(name="Private", workflow=workflow)
    public = State.objects.create(name="Public", workflow=workflow)

    # Create transitions
    make_public = Transition.objects.create(name="Make public", workflow=workflow, destination = public)
    make_private = Transition.objects.create(name="Make private", workflow=workflow, destination = private)

    # Add transitions
    private.transitions.add(make_public)
    public.transitions.add(make_private)

    # Add all permissions which are managed by the workflow
    WorkflowPermissionRelation.objects.create(workflow=workflow, permission=add)
    WorkflowPermissionRelation.objects.create(workflow=workflow, permission=delete)
    WorkflowPermissionRelation.objects.create(workflow=workflow, permission=edit)
    WorkflowPermissionRelation.objects.create(workflow=workflow, permission=view)

    # Add permissions for single states

    # Private
    StatePermissionRelation.objects.create(state=private, permission=add, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=delete, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=edit, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=view, role=owner)

    StatePermissionRelation.objects.create(state=private, permission=add, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=delete, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=edit, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=view, role=manager)

    # Public
    StatePermissionRelation.objects.create(state=public, permission=view, role=anonymous)

    StatePermissionRelation.objects.create(state=public, permission=view, role=editor)

    StatePermissionRelation.objects.create(state=public, permission=view, role=reader)

    StatePermissionRelation.objects.create(state=public, permission=view, role=reviewer)

    StatePermissionRelation.objects.create(state=public, permission=add, role=owner)
    StatePermissionRelation.objects.create(state=public, permission=delete, role=owner)
    StatePermissionRelation.objects.create(state=public, permission=edit, role=owner)
    StatePermissionRelation.objects.create(state=public, permission=view, role=owner)

    StatePermissionRelation.objects.create(state=public, permission=add, role=manager)
    StatePermissionRelation.objects.create(state=public, permission=delete, role=manager)
    StatePermissionRelation.objects.create(state=public, permission=edit, role=manager)
    StatePermissionRelation.objects.create(state=public, permission=view, role=manager)

    # Add inheritance block for single states
    StateInheritanceBlock.objects.create(state=private, permission=add)
    StateInheritanceBlock.objects.create(state=private, permission=delete)
    StateInheritanceBlock.objects.create(state=private, permission=edit)
    StateInheritanceBlock.objects.create(state=private, permission=view)

    StateInheritanceBlock.objects.create(state=public, permission=add)
    StateInheritanceBlock.objects.create(state=public, permission=delete)
    StateInheritanceBlock.objects.create(state=public, permission=edit)
    StateInheritanceBlock.objects.create(state=public, permission=view)

    # Define public state
    WorkflowStatesInformation.objects.create(state=public, public=True)

    # Define initial state
    workflow.initial_state = private
    workflow.save()

    # Portal Workflow
    ##########################################################################

    # Add workflow
    portal_workflow, created = Workflow.objects.get_or_create(name="Portal")

    # Add states
    private = State.objects.create(name="Private", workflow=portal_workflow)
    submitted = State.objects.create(name="Submitted", workflow=portal_workflow)
    public = State.objects.create(name="Public", workflow=portal_workflow)

    # Create transitions
    submit_t = Transition.objects.create(name="Submit", workflow=portal_workflow, destination = submitted)
    make_public = Transition.objects.create(name="Make public", workflow=portal_workflow, destination = public)
    make_private = Transition.objects.create(name="Make private", workflow=portal_workflow, destination = private)
    reject = Transition.objects.create(name="Reject", workflow=portal_workflow, destination = private)

    # Add transitions
    private.transitions.add(submit_t)
    submitted.transitions.add(make_public)
    submitted.transitions.add(reject)
    public.transitions.add(make_private)

    # Add all permissions which are managed by the workflow
    WorkflowPermissionRelation.objects.create(workflow=portal_workflow, permission=add)
    WorkflowPermissionRelation.objects.create(workflow=portal_workflow, permission=delete)
    WorkflowPermissionRelation.objects.create(workflow=portal_workflow, permission=edit)
    WorkflowPermissionRelation.objects.create(workflow=portal_workflow, permission=view)

    # Add permissions for single states

    # Private
    StatePermissionRelation.objects.create(state=private, permission=add, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=delete, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=edit, role=owner)
    StatePermissionRelation.objects.create(state=private, permission=view, role=owner)

    StatePermissionRelation.objects.create(state=private, permission=add, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=delete, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=edit, role=manager)
    StatePermissionRelation.objects.create(state=private, permission=view, role=manager)

    StateInheritanceBlock.objects.create(state=private, permission=add)
    StateInheritanceBlock.objects.create(state=private, permission=delete)
    StateInheritanceBlock.objects.create(state=private, permission=edit)
    StateInheritanceBlock.objects.create(state=private, permission=view)

    # Submitted
    StatePermissionRelation.objects.create(state=submitted, permission=view, role=owner)

    StatePermissionRelation.objects.create(state=submitted, permission=add,    role=manager)
    StatePermissionRelation.objects.create(state=submitted, permission=delete, role=manager)
    StatePermissionRelation.objects.create(state=submitted, permission=edit,   role=manager)
    StatePermissionRelation.objects.create(state=submitted, permission=view,   role=manager)

    StatePermissionRelation.objects.create(state=submitted, permission=add,    role=reviewer)
    StatePermissionRelation.objects.create(state=submitted, permission=delete, role=reviewer)
    StatePermissionRelation.objects.create(state=submitted, permission=edit,   role=reviewer)
    StatePermissionRelation.objects.create(state=submitted, permission=view,   role=reviewer)

    StateInheritanceBlock.objects.create(state=submitted, permission=add)
    StateInheritanceBlock.objects.create(state=submitted, permission=delete)
    StateInheritanceBlock.objects.create(state=submitted, permission=edit)
    StateInheritanceBlock.objects.create(state=submitted, permission=view)

    # Public
    StatePermissionRelation.objects.create(state=public, permission=add,    role=manager)
    StatePermissionRelation.objects.create(state=public, permission=delete, role=manager)
    StatePermissionRelation.objects.create(state=public, permission=edit,   role=manager)
    StatePermissionRelation.objects.create(state=public, permission=view,   role=manager)

    StatePermissionRelation.objects.create(state=public, permission=view, role=reader)

    StateInheritanceBlock.objects.create(state=public, permission=add)
    StateInheritanceBlock.objects.create(state=public, permission=delete)
    StateInheritanceBlock.objects.create(state=public, permission=edit)

    # Define public state
    WorkflowStatesInformation.objects.create(state=public, public=True)

    # Define review state
    WorkflowStatesInformation.objects.create(state=submitted, review=True)

    # Define initial state
    portal_workflow.initial_state = private
    portal_workflow.save()

    # Set workflow for Page
    ctype = ContentType.objects.get_for_model(Page)
    workflows.utils.set_workflow_for_model(ctype, portal_workflow)

def run():
    load_data()