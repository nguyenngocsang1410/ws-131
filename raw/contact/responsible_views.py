#!/usr/bin/env powerscript
# coding: utf-8
#
# Copyright (C) 1990 - 2026 CONTACT Software GmbH
# All rights reserved.
# http://www.contact-software.com
# pylint: disable=too-many-positional-arguments

"""
Generates views for "responsible" catalogs implemented in ``cs.workflow.responsible``.
Each view consists of these fields:

=== =============== =================================================================
No. Field Name      Description
=== =============== =================================================================
1.  subject_uuid    UUID for assigning subject to system task classification property
2.  subject_type    Context role identifier
3.  subject_type_XX (XX = isocode of any language) Context role identifier UI name
4.  subject_id      ID unique for given ``subject_type`` and ``subject_id2``
5.  subject_id2     Context ID (empty string for "Person" and "Common Role")
6.  order_by        Constant number, entries are sorted by ascending value
x.  name_XX         (XX = isocode of any UI language) UI name from role def
y.  description_XX  (XX = isocode of any UI language) Additional info from role def
z.  first-/lastname first or last name from role def
=== =============== =================================================================

Notes:
- ``subject_uuid`` will be ``NULL`` if the data source is missing the ``cdb_object_id`` field.
  In this case, this context's roles cannot be used for system tasks.
- Because ``cdbwf_responsible_template`` only uses context role _definitions_,
  ``subject_id2`` is always empty in this view.

"""

from cdb import ddl, i18n, sqlapi
from cdb.objects.org import Person
from cdb.platform.mom.entities import View
from cdb.platform.mom.fields import DDMultiLangField
from cs.workflow.subjects import get_context_ml_field_names, get_contexts

WHERE = {
    "angestellter": """
            active_account='1'
            AND visibility_flag=1
            AND (is_system_account=0 OR is_system_account IS NULL)""",
    "cdb_global_role": "is_org_role = 1",
    "*": "obsolete = 0",  # fallback for any context
}
FIELD_NAMES = {  # name field, description field
    "angestellter": ("name", "remarks"),
    "cdb_global_role": ("name", "description_ml"),
    "*": ("name_ml", "description_ml"),  # fallback for any context
}
ORDER_BY = {
    "Person": "",  # 1st
    "Common Role": " ",  # 2nd
    # others map to their key value -> are sorted last
}


def get_collation():
    """
    :returns: Collate statement for use with constant values in MS SQL
    :rtype: str
    """
    if sqlapi.SQLdbms() == sqlapi.DBMS_MSSQL:
        from cdb.mssql import CollationDefault

        return f" COLLATE {CollationDefault.get_default_collation()} "
    return ""


def generate_cdbwf_responsible_template():
    """
    :returns: Select statement to generate view ``cdbwf_responsible_template`` combining
        - users
        - global roles
        - context role definitions
    :rtype: str
    """
    return _get_statement(*_get_contexts(True))


def generate_cdbwf_responsible():
    """
    :returns: Select statement to generate view ``cdbwf_responsible`` combining
        - users
        - global roles
        - context roles
    :rtype: str
    """
    return _get_statement(*_get_contexts(False))


def _get_contexts(is_template):
    contexts = get_contexts()
    sorted_contexts = sorted(contexts, key=lambda x: ORDER_BY.get(x, x))

    for index, subject_type in enumerate(sorted_contexts):
        (role_def_class, role_class, ctx_attr, _) = contexts[subject_type]
        _class = role_def_class if is_template else role_class
        field_name = _class.GetTablePKeys()[0].name
        yield (
            _class,
            role_def_class,
            field_name,
            None if is_template else ctx_attr,
            subject_type,
            index + 1,
        )


def _get_statement(*parts):
    return " UNION ".join(_get_partial_statement(*part) for part in parts)


def _get_partial_statement(
    role_class, role_def_class, subj_id_field, subj_id2_field, subject_type, order_by
):
    collation = get_collation()
    classname = role_class().GetClassname()
    table_name = role_class.GetTableName()
    subject_id2 = f"{table_name}.{subj_id2_field}" if subj_id2_field else "''"

    if role_class == role_def_class:
        join = ""
        name_ml = _get_multilang(table_name, classname, True, None, None)
        desc_ml = _get_multilang(table_name, classname, False, None, None)
    else:
        def_table = role_def_class.GetTableName()
        def_classname = role_def_class().GetClassname()
        def_pkey = role_def_class.GetTablePKeys()[0].name
        join = f"""
        LEFT JOIN {def_table}
            ON {def_table}.{def_pkey} = {table_name}.role_id"""
        name_ml = _get_multilang(table_name, classname, True, def_table, def_classname)
        desc_ml = _get_multilang(table_name, classname, False, def_table, def_classname)

    # subject_uuid is required to assign subjects to system task classification properties
    if ddl.Table(table_name).hasColumn("cdb_object_id"):
        subject_uuid = f"{table_name}.cdb_object_id"
    else:
        subject_uuid = "''"

    if ddl.Table(table_name).hasColumn("firstname"):
        firstname = f"{table_name}.firstname"
        lastname = f"{table_name}.lastname"
    else:
        firstname = "''"
        lastname = "''"

    return f"""
        SELECT
            {subject_uuid} AS subject_uuid,
            '{subject_type}' {collation} AS subject_type,
            {_get_multilang_type(subject_type, collation)},
            {table_name}.{subj_id_field} AS subject_id,
            {subject_id2} {collation} AS subject_id2,
            {order_by} AS order_by,
            {name_ml},
            {firstname} AS firstname,
            {lastname} AS lastname,
            {desc_ml}
        FROM {table_name}{join}
        WHERE {WHERE.get(table_name, WHERE["*"])}
    """


def _get_multilang_type(subject_type, collation):
    type_map = get_context_ml_field_names(subject_type)

    fallback_value = (
        type_map.get("vi")
        or type_map.get("en")
        or type_map.get("de")
        or next(iter(type_map.values()))
    )

    return ",\n".join(
        f"            '{type_map.get(isocode, fallback_value)}' {collation} AS subject_type_{isocode}"
        for isocode in i18n.Languages()
    )


def _get_multilang(table_name, classname, is_name, def_table_name, def_classname):
    view_field_name = "name" if is_name else "description"
    field_name = FIELD_NAMES.get(table_name, FIELD_NAMES["*"])[int(not is_name)]

    if table_name == Person.__maps_to__:
        # persons are not internationalized
        field_map = {isocode: field_name for isocode in i18n.Languages()}
    else:
        ml_field = DDMultiLangField.ByKeys(def_classname or classname, field_name)
        field_map = {x.cdb_iso_language_code: x.field_name for x in ml_field.LangFields}

        fallback_field = (
            field_map.get("vi")
            or field_map.get("en")
            or field_map.get("de")
            or next(iter(field_map.values()))
        )

        field_map = {
            isocode: field_map.get(isocode, fallback_field)
            for isocode in i18n.Languages()
        }

    return ",\n            ".join(
        f"{def_table_name or table_name}.{field_map[isocode]} AS {view_field_name}_{isocode}"
        for isocode in i18n.Languages()
    )


def compile_views():
    for view in View.KeywordQuery(
        classname=["cdbwf_responsible", "cdbwf_responsible_template"]
    ):
        view.compile()
