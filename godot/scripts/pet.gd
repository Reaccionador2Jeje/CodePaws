extends Node3D
class_name CodePawsPet

@export var pet_name: String = "Py"
@export var body_color: Color = Color(0.25, 0.72, 0.43)
@export var wander_radius: float = 7.0

var happiness: int = 80
var cleanliness: int = 90
var hunger: int = 20
var energy: int = 100
var _home: Vector3
var _target: Vector3
var _wander_timer: float = 0.0
var _bob_time: float = 0.0
var _body: MeshInstance3D
var _need_timer: float = 0.0

func _ready() -> void:
	add_to_group("pets")
	_home = global_position
	_target = _home
	_build_mascot()

func _build_mascot() -> void:
	_body = MeshInstance3D.new()
	var body_mesh := SphereMesh.new()
	body_mesh.radius = 0.58
	body_mesh.height = 1.16
	_body.mesh = body_mesh
	var material := StandardMaterial3D.new()
	material.albedo_color = body_color
	material.roughness = 0.78
	_body.material_override = material
	_body.position.y = 0.65
	add_child(_body)

	var face := MeshInstance3D.new()
	var face_mesh := SphereMesh.new()
	face_mesh.radius = 0.38
	face_mesh.height = 0.76
	face.mesh = face_mesh
	var face_material := StandardMaterial3D.new()
	face_material.albedo_color = body_color.lightened(0.16)
	face.material_override = face_material
	face.position = Vector3(0.0, 0.83, -0.36)
	face.scale = Vector3(1.0, 0.8, 0.7)
	add_child(face)

	for eye_x in [-0.14, 0.14]:
		var eye := MeshInstance3D.new()
		var eye_mesh := SphereMesh.new()
		eye_mesh.radius = 0.045
		eye_mesh.height = 0.09
		eye.mesh = eye_mesh
		var eye_material := StandardMaterial3D.new()
		eye_material.albedo_color = Color(0.06, 0.08, 0.1)
		eye.material_override = eye_material
		eye.position = Vector3(eye_x, 0.9, -0.69)
		add_child(eye)

func _process(delta: float) -> void:
	_bob_time += delta
	_body.position.y = 0.65 + sin(_bob_time * 3.0) * 0.045
	_need_timer += delta
	if _need_timer >= 20.0:
		_need_timer = 0.0
		hunger = mini(100, hunger + 2)
		happiness = maxi(0, happiness - 1)
		energy = maxi(0, energy - 1)

	_wander_timer -= delta
	if _wander_timer <= 0.0 or global_position.distance_to(_target) < 0.35:
		_target = _home + Vector3(
			randf_range(-wander_radius, wander_radius), 0.0,
			randf_range(-wander_radius, wander_radius)
		)
		_wander_timer = randf_range(2.5, 5.0)
	var direction := _target - global_position
	direction.y = 0.0
	if direction.length() > 0.25 and energy > 5:
		global_position += direction.normalized() * 1.2 * delta
		look_at(global_position + direction, Vector3.UP)

func interact() -> String:
	happiness = mini(100, happiness + 12)
	cleanliness = mini(100, cleanliness + 1)
	return "%s está feliz de pasar tiempo contigo. Felicidad: %d%%" % [pet_name, happiness]

func feed() -> String:
	hunger = maxi(0, hunger - 25)
	happiness = mini(100, happiness + 3)
	return "¡%s ha comido! Hambre: %d%%" % [pet_name, hunger]

func to_save_data() -> Dictionary:
	return {
		"name": pet_name,
		"position": [global_position.x, global_position.y, global_position.z],
		"happiness": happiness,
		"cleanliness": cleanliness,
		"hunger": hunger,
		"energy": energy
	}

func load_save_data(data: Dictionary) -> void:
	var saved_position: Array = data.get("position", [global_position.x, global_position.y, global_position.z])
	if saved_position.size() == 3:
		global_position = Vector3(float(saved_position[0]), float(saved_position[1]), float(saved_position[2]))
		_home = global_position
	happiness = clampi(int(data.get("happiness", happiness)), 0, 100)
	cleanliness = clampi(int(data.get("cleanliness", cleanliness)), 0, 100)
	hunger = clampi(int(data.get("hunger", hunger)), 0, 100)
	energy = clampi(int(data.get("energy", energy)), 0, 100)
