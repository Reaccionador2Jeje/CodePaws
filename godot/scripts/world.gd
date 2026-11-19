extends Node3D

const PlayerScript = preload("res://scripts/player.gd")
const PetScript = preload("res://scripts/pet.gd")

var _message_label: Label
var _nearby_pet: CodePawsPet
var _message_timer: float = 0.0

func _ready() -> void:
	randomize()
	_build_environment()
	_build_world()
	_spawn_player()
	_spawn_pets()
	_build_hud()

func _process(delta: float) -> void:
	_message_timer = maxf(0.0, _message_timer - delta)
	_nearby_pet = null
	var player := get_tree().get_first_node_in_group("player") as Node3D
	if player:
		var closest := 3.2
		for pet in get_tree().get_nodes_in_group("pets"):
			var distance := player.global_position.distance_to(pet.global_position)
			if distance < closest:
				closest = distance
				_nearby_pet = pet as CodePawsPet
	if Input.is_action_just_pressed("interact") and _nearby_pet:
		_show_message(_nearby_pet.interact())
	elif _message_timer <= 0.0:
		if _nearby_pet:
			_message_label.text = "F  ·  Interactuar con " + _nearby_pet.pet_name
		else:
			_message_label.text = "WASD · Mover    ESPACIO · Saltar    F · Interactuar    ESC · Liberar mouse"

func _build_environment() -> void:
	var world_environment := WorldEnvironment.new()
	var environment := Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var sky_material := ProceduralSkyMaterial.new()
	sky_material.sky_top_color = Color(0.20, 0.43, 0.68)
	sky_material.sky_horizon_color = Color(0.72, 0.84, 0.91)
	sky_material.ground_bottom_color = Color(0.18, 0.25, 0.20)
	sky_material.ground_horizon_color = Color(0.62, 0.70, 0.58)
	sky.sky_material = sky_material
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.72, 0.79, 0.86)
	environment.ambient_light_energy = 0.75
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	world_environment.environment = environment
	add_child(world_environment)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -32.0, 0.0)
	sun.light_energy = 1.25
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 55.0
	add_child(sun)

func _build_world() -> void:
	_add_box("Ground", Vector3(0, -0.55, 0), Vector3(150, 1, 150), Color(0.28, 0.55, 0.31), true)
	_add_box("Village path", Vector3(0, 0.015, 0), Vector3(9, 0.08, 100), Color(0.72, 0.62, 0.43), false)
	_add_box("Cross path", Vector3(0, 0.02, -5), Vector3(75, 0.08, 7), Color(0.72, 0.62, 0.43), false)
	_add_box("Pond", Vector3(24, 0.0, 15), Vector3(17, 0.12, 13), Color(0.20, 0.57, 0.76), false)
	_build_house(Vector3(-13, 0.0, -11))
	_build_house(Vector3(16, 0.0, -23))
	for i in range(65):
		var x := randf_range(-65.0, 65.0)
		var z := randf_range(-65.0, 65.0)
		if absf(x) < 8.0 or (absf(x + 13.0) < 10.0 and absf(z + 11.0) < 9.0):
			continue
		_build_tree(Vector3(x, 0.0, z), randf_range(0.8, 1.35))

func _build_house(origin: Vector3) -> void:
	_add_box("House walls", origin + Vector3(0, 2.0, 0), Vector3(9, 4, 8), Color(0.91, 0.78, 0.59), true)
	_add_box("Roof", origin + Vector3(0, 4.5, 0), Vector3(10, 1, 9), Color(0.63, 0.27, 0.22), false)
	_add_box("Door", origin + Vector3(0, 1.0, -4.06), Vector3(1.5, 2, 0.12), Color(0.34, 0.20, 0.13), false)
	_add_box("Window", origin + Vector3(-2.6, 2.5, -4.08), Vector3(1.5, 1.3, 0.12), Color(0.38, 0.72, 0.83), false)

func _build_tree(origin: Vector3, scale_factor: float) -> void:
	var trunk := MeshInstance3D.new()
	var trunk_mesh := CylinderMesh.new()
	trunk_mesh.top_radius = 0.22 * scale_factor
	trunk_mesh.bottom_radius = 0.34 * scale_factor
	trunk_mesh.height = 2.0 * scale_factor
	trunk.mesh = trunk_mesh
	trunk.position = origin + Vector3(0, scale_factor, 0)
	trunk.material_override = _material(Color(0.37, 0.23, 0.13))
	add_child(trunk)
	var crown := MeshInstance3D.new()
	var crown_mesh := SphereMesh.new()
	crown_mesh.radius = 1.35 * scale_factor
	crown_mesh.height = 2.7 * scale_factor
	crown.mesh = crown_mesh
	crown.position = origin + Vector3(0, 2.5 * scale_factor, 0)
	crown.material_override = _material(Color(0.16 + randf() * 0.08, 0.42 + randf() * 0.12, 0.22))
	add_child(crown)

func _spawn_player() -> void:
	var player := PlayerScript.new() as CharacterBody3D
	player.position = Vector3(0, 0.1, 8)
	add_child(player)

func _spawn_pets() -> void:
	var definitions := [
		["Py", Color(0.25, 0.68, 0.39), Vector3(-3, 0, 2)],
		["Ferris", Color(0.85, 0.30, 0.22), Vector3(3, 0, 0)],
		["Gopher", Color(0.28, 0.62, 0.82), Vector3(-5, 0, -4)],
		["Duke", Color(0.82, 0.48, 0.23), Vector3(5, 0, -5)]
	]
	for definition in definitions:
		var pet := PetScript.new() as Node3D
		pet.pet_name = definition[0]
		pet.body_color = definition[1]
		pet.position = definition[2]
		add_child(pet)

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var title := Label.new()
	title.text = "CODEPAWS 3D  ·  EARLY WORLD"
	title.position = Vector2(24, 18)
	title.add_theme_font_size_override("font_size", 25)
	title.add_theme_color_override("font_color", Color(1.0, 0.96, 0.83))
	layer.add_child(title)
	_message_label = Label.new()
	_message_label.position = Vector2(24, 665)
	_message_label.add_theme_font_size_override("font_size", 17)
	_message_label.add_theme_color_override("font_color", Color.WHITE)
	layer.add_child(_message_label)
	var hint := Label.new()
	hint.text = "EXPLORA · CONOCE A TUS MASCOTAS · DESCUBRE EL VALLE"
	hint.position = Vector2(24, 55)
	hint.add_theme_font_size_override("font_size", 13)
	hint.add_theme_color_override("font_color", Color(0.85, 0.94, 0.89))
	layer.add_child(hint)

func _show_message(message: String) -> void:
	_message_label.text = message
	_message_timer = 3.0

func _add_box(object_name: String, position: Vector3, size: Vector3, color: Color, solid: bool) -> void:
	var body := StaticBody3D.new() if solid else Node3D.new()
	body.name = object_name
	body.position = position
	var mesh_instance := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh_instance.mesh = box
	mesh_instance.material_override = _material(color)
	body.add_child(mesh_instance)
	if solid:
		var collision := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = size
		collision.shape = shape
		body.add_child(collision)
	add_child(body)

func _material(color: Color) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.9
	return material
