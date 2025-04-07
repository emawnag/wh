let renderer, scene, camera
let cameraControl, stats, gui

// points
const pointCount = 10000
const movementSpeed = 20
let explosion
let size = 20
const textureLoader = new THREE.TextureLoader()
const smokeTexture = textureLoader.load('./smoke.png')
// Add OBJLoader
const objLoader = new THREE.OBJLoader()
let whale // Variable to store the loaded whale model

// URL hash parameters
let urlParams = {}
let statusCheckURL = '127.0.0.1:20597/status'
let cleanMode = false
let statusCheckInterval = null

// Parse URL hash parameters
function parseHashParams() {
  const hash = window.location.hash.substring(1)
  if (!hash) return {}
  
  try {
    // Check if it's base64 encoded
    const decoded = atob(hash)
    return JSON.parse(decoded)
  } catch (e) {
    // If not base64, try regular parsing
    const params = {}
    hash.split('&').forEach(param => {
      const [key, value] = param.split('=')
      if (key && value) {
        params[key.trim()] = value.trim()
      }
    })
    return params
  }
}

var hadBeenTriggered = false;
// Check status from URL
function checkStatus() {
  if (hadBeenTriggered===false&& (urlParams.clean === 'true' || urlParams.clean === true)) {
  fetch(`http://${statusCheckURL}`)
    .then(response => response.json()) // Parse response as JSON
    .then(data => {
      if (data.trigger && controls) {
        hadBeenTriggered = true;
        controls.explosionTrigger();
      }
      //if (whale) {
        // Apply scale and translation to the whale
        //whale.scale.set(data.scale, data.scale, data.scale);
        //whale.position.set(data.translateX, data.translateY, whale.position.z);
      //}
    })
    .catch(error => console.error('Status check error:', error))
}
}

// Add MTLLoader along with OBJLoader
const mtlLoader = new THREE.MTLLoader()

function loadWhaleModel() {
  // Add a loading indicator
  console.log('Loading whale model...')
  
  // First load the material file
  mtlLoader.setPath('./wh/')
  mtlLoader.load(
    'Whale_Quad.mtl',
    function(materials) {
      materials.preload();
      
      // Set texture path to the correct location
      // materials.materials.Whale_Quad_Material.map.image.src = './wh/Textures/Whale_Quad_Diffuse.png';
      // if (materials.materials.Whale_Quad_Material.roughnessMap) {
      //   materials.materials.Whale_Quad_Material.roughnessMap.image.src = './wh/Textures/Whale_Quad_Roughness.png';
      // }
      // if (materials.materials.Whale_Quad_Material.normalMap) {
      //   materials.materials.Whale_Quad_Material.normalMap.image.src = './wh/Textures/Whale_Quad_Normal.png';
      // }
      
      // After material is loaded, configure the object loader to use it
      objLoader.setMaterials(materials);
      objLoader.setPath('./wh/');
      
      // Now load the object with materials applied
      objLoader.load(
        'Whale_Quad.obj', 
        function(object) {
          // Position the whale at 0, 0, 0
          object.position.set(0, 0, 0)
          
          // Scale the whale to be more visible
          object.scale.set(20, 20, 20)
          
          whale = object
          scene.add(whale)
          console.log('Whale model loaded successfully')
        },
        function(xhr) {
          console.log('Whale model ' + (xhr.loaded / xhr.total * 100) + '% loaded')
        },
        function(error) {
          console.error('Error loading whale model:', error)
        }
      )
    },
    undefined,
    function(error) {
      console.error('Error loading materials:', error);
    }
  )
}


function initStats() {
  const stats = new Stats()
  stats.setMode(0)
  document.getElementById('stats').appendChild(stats.domElement)
  return stats
}

// dat.GUI
let controls = new (function() {
  this.explosionTrigger = function() {
    if (explosion) {
      explosion.destroy()
    }
    explosion = new Explosion(this.whaleX, this.whaleY, this.whaleZ)
    
    // Hide the whale when explosion is triggered
    if (whale) {
      whale.visible = false
    }
  }
  this.pointSize = 20
  this.cameraNear = 500
  // this.pointCount = 1000
  
  // Add light position controls
  this.lightX = -0.4
  this.lightY = -1.3
  this.lightZ = 10
  
  // Add whale position controls
  this.whaleX = 0
  this.whaleY = 0
  this.whaleZ = 0
  
  // Reset whale position to center
  this.resetWhalePosition = function() {
    this.whaleX = 0
    this.whaleY = 0
    this.whaleZ = 0
    if (whale) {
      whale.position.set(this.whaleX, this.whaleY, this.whaleZ)
    }
  }
})()

// 建立粒子系統
class Explosion {
  constructor(x, y, z) {
    const geometry = new THREE.Geometry()

    this.material = new THREE.PointsMaterial({
      size: size,
      color: new THREE.Color(Math.random() * 0xffffff),
      map: smokeTexture,
      blending: THREE.AdditiveBlending,
      depthTest: false
      // transparent: true,
      // opacity: 0.7
    })

    this.pCount = pointCount
    this.movementSpeed = movementSpeed
    this.dirs = []

    for (let i = 0; i < this.pCount; i++) {
      const vertex = new THREE.Vector3(x, y, z) // 每個頂點起點都在爆炸起源點
      geometry.vertices.push(vertex)
      const r = this.movementSpeed * THREE.Math.randFloat(0, 1) + 2
      // 噴射方向隨機 -> 不規則球體
      const theta = Math.random() * Math.PI * 2
      const phi = Math.random() * Math.PI
      this.dirs.push({
        x: r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.sin(phi) * Math.sin(theta),
        z: r * Math.cos(phi)
      })
      // 噴射方向隨機 -> 正方體
      // this.dirs.push({
      //   x: Math.random() * r - r / 2,
      //   y: Math.random() * r - r / 2,
      //   z: Math.random() * r - r / 2
      // })
    }

    let points = new THREE.Points(geometry, this.material)

    this.object = points

    scene.add(this.object)
  }

  update() {
    let p = this.pCount
    const d = this.dirs
    while (p--) {
      let particle = this.object.geometry.vertices[p]
      // 每個頂點往自己噴射方向一直移動，會漸漸淡出是也可見範圍，但他仍一直在運動
      particle.x += d[p].x
      particle.y += d[p].y
      particle.z += d[p].z
    }
    this.object.geometry.verticesNeedUpdate = true
  }

  destroy() {
    this.object.geometry.dispose()
    scene.remove(this.object)
    // console.log(renderer.info)
    this.dirs.length = 0
  }
}

function init() {
  // Get URL parameters from hash
  urlParams = parseHashParams()
  
  // Set clean mode if specified
  if (urlParams.clean === 'true' || urlParams.clean === true) {
    cleanMode = true
  }
  
  // Set status check URL if specified
  if (urlParams.listenURL) {
    statusCheckURL = urlParams.listenURL
  }
  
  // scene
  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x000000, 0.0008)

  // camera
  camera = new THREE.PerspectiveCamera(
    70,
    window.innerWidth / window.innerHeight,
    500,
    5000
  )
  camera.position.set(0, 0, 1000)
  camera.lookAt(scene.position)

  // Add lights so we can see the whale
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.0); 
  scene.add(ambientLight);
 
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
  directionalLight.position.set(controls.lightX, controls.lightY, controls.lightZ);
  scene.add(directionalLight);

  // renderer
  renderer = new THREE.WebGLRenderer({ alpha: true })
  renderer.setClearColor(0x000000, 0)
  renderer.setSize(window.innerWidth, window.innerHeight)

  // Load the whale model
  loadWhaleModel();

  // Only initialize stats and GUI if not in clean mode
  if (!cleanMode) {
    // stats
    stats = initStats()
    
    // dat.GUI
    gui = new dat.GUI()
    gui.add(controls, 'explosionTrigger')
    gui.add(controls, 'pointSize', 10, 200).onChange(e => {
      size = e
    })
    gui.add(controls, 'cameraNear', 1, 1000).onChange(near => {
      camera = new THREE.PerspectiveCamera(
        70,
        window.innerWidth / window.innerHeight,
        near,
        5000
      )
      camera.position.set(0, 0, 1000)
      camera.lookAt(scene.position)
    })
    
    // Add light position controls
    const lightFolder = gui.addFolder('Light Position')
    lightFolder.add(controls, 'lightX', -10, 10).onChange(value => {
      directionalLight.position.x = value
    })
    lightFolder.add(controls, 'lightY', -10, 10).onChange(value => {
      directionalLight.position.y = value
    })
    lightFolder.add(controls, 'lightZ', -10, 20).onChange(value => {
      directionalLight.position.z = value
    })
    lightFolder.open()
    
    // Add whale position controls
    const whaleFolder = gui.addFolder('Whale Position')
    whaleFolder.add(controls, 'whaleX', -100, 100).onChange(value => {
      if (whale) {
        whale.position.x = value
      }
    })
    whaleFolder.add(controls, 'whaleY', -100, 100).onChange(value => {
      if (whale) {
        whale.position.y = value
      }
    })
    whaleFolder.add(controls, 'whaleZ', -100, 100).onChange(value => {
      if (whale) {
        whale.position.z = value
      }
    })
    whaleFolder.add(controls, 'resetWhalePosition')
    whaleFolder.open()
  } else {
    // Hide stats element in clean mode
    const statsEl = document.getElementById('stats')
    if (statsEl) {
      statsEl.style.display = 'none'
    }
  }

  document.body.appendChild(renderer.domElement)
}

function render() {
  if (explosion) {
    explosion.update()
  }

  if (stats) {
    stats.update()
  }
  
  requestAnimationFrame(render)
  // cameraControl.update()
  renderer.render(scene, camera)
}

window.addEventListener('resize', function() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
})

// Initialize status checking when document is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Start polling status URL every 100ms
  statusCheckInterval = setInterval(checkStatus, 100);
});

init()
render()
