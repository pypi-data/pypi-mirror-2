
Entity management
=================

In the `home page <TERENAPEERDOMAIN/>`_ of the site there is a link, labelled "Full list of entities", that takes the user to a `paginated list of all entities <TERENAPEERDOMAIN/entity/>`_, regardless of their owners. In this page the user can add a new entity, if she follows the link labelled "Add entity". In the form presented thereafter she will only have to provide a name for the new entity and select a domain for it. From the list of entities a user can also click on an entity to view its details. If she she is visiting the site as an authenticated user, in this entity detail page she will be presented with a menu that allows her to manage the entity. This menu presents the following links:

 * `Details`: The detail page for the entity, the same that is accessed by clicking on its name from the listing of all entities.
 * `Modify`: XXX 
 * `Edit metadata`: This link takes the user to a view that allows her to edit the metadata for the entity. There are 3 ways of editing these metadata, as we shall see bellow in the section "Metadata edition".
 * `Remove`: This link is used to completely remove the entity from the database. Clicking on it will take the user to a confirmation page, and confirmation will delete the entity.
 * `Team permissions`: XXX

Metadata edition
----------------

The metadata of an entity consists of an XML document (XXX schema) that describes the public endpoint represented by the entity. There are three ways to edit the metadata of an entity. All three of them are accessible from the "Edit metadata" page for the entity.

 * `By text editing`: The user is presented with a text area with the XML document, where she can directly edit the XML.
 * `By uploading a file`: The user is presented with a file input, through which she can upload a file with the new XML metadata document.
 * `By fetching a remote URL`: If the metadata is published elsewhere in the network, the user can use this form to provide the URL of the published XML metadata document. The system will download the document pointed at by the URL and use it as metadata for the entity.

In all three cases, changing the metadata will create a new revision of the document that contains it. In the three forms there is a text input labelled "commit message", and the text entered in this input will be associated with the new revision, and used to identify it.

All the inputs in these forms (two inputs in each form, one for the metadata and one for the commit message) are required: leaving one of them empty will trigger a validation error, and the user will be prompted to fill in the missing value. Additionally, the system will check that the entered metadata (irrespective of the method used to enter it) is valid XML, (XXX and conforms to the DTD / XML Schema), and if it isn't valid, (XXX or doesn't conform), the metadata will not be saved and the user will be prompted to enter correct values, with indications, whenever possible, of the detected errors.


XXX the metadata is not yet on the form or the detail page.
XXX search entities
