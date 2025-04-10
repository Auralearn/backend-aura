"""
TODO:

1. Create a route to get materials
# Route: /materials
# Method: GET
# Request Body: None
# Response Body: JSON object containing a list of materials
[
  {"id": "<unique_code>", "title": "Matematika - Kelas 1 SD"},
  {"id": "<unique_code>", "title": "Matematika - Kelas 2 SD"},
  ...
]

2. Create a route to get material content
# Route: /materials/<material_id>
# Method: GET
# Request Body: None
# Response Body: JSON object containing the content of the material
{
  "id": "<unique_code>",
  "title": "Matematika - Kelas 1 SD",
  "content": "..."
}
"""