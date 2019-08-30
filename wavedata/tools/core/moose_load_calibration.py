
import yaml
import numpy as np

def load_calibration(calib_path):
  calib = {};

  # Get calibrations
  calib['extrinsics'] = yaml.load(open(calib_path + '/extrinsics.yaml'));
  #camera's extrinsic matrix describes the camera's location in the world and what direction it's pointing

  calib['CAM00'] = yaml.load(open(calib_path + '/F.yaml')); #intrinsic matrix
  calib['CAM01'] = yaml.load(open(calib_path + '/FR.yaml'));
  calib['CAM02'] = yaml.load(open(calib_path + '/RF.yaml'));
  calib['CAM03'] = yaml.load(open(calib_path + '/RB.yaml'));
  calib['CAM04'] = yaml.load(open(calib_path + '/B.yaml'));
  calib['CAM05'] = yaml.load(open(calib_path + '/LB.yaml'));
  calib['CAM06'] = yaml.load(open(calib_path + '/LF.yaml'));
  calib['CAM07'] = yaml.load(open(calib_path + '/FL.yaml'));

  '''
  example:
  print(calib['CAM00']):
  {'image_height': 1024, 'distortion_coefficients': {'rows': 1, 'data': [-0.211078226790761, 0.101157542400588, -0.00032951581724786, 0.000330423801388672, -0.0232053947325804], 'cols': 5}, 'camera_name': 'camera_F', 'image_width': 1280, 'camera_matrix': {'rows': 3, 'data': [653.956033188809, -0.235925653043616, 653.221172545916, 0, 655.54008861796, 508.732863993917, 0, 0, 1], 'cols': 3}, 'distortion_model': 'plumb_bob'}

  '''

  # testing
  # calib['extrinsics']['T_LIDAR_FCAMERA'] = np.array([
  #   [0.0242754, -0.0154538, 0.999586, 0.54965],
  #   [-0.999678, 0.0069789, 0.0243855, 0.0207935],
  #   [-0.00735294, -0.999856, -0.0152794, -0.62072],
  #   [0.0,0.0,0.0,1.0,]
  #   ]);

  #Extrinsic matrix describes how to transform points in world coordinates to camera coordinates

  # Precompute T_LIDAR_CAM## matrixes
  '''
  the following will not be used
  calib['extrinsics']['T_LIDAR_CAM00'] = calib['extrinsics']['T_LIDAR_FCAMERA']; #from lidar to the front camera

  calib['extrinsics']['T_LIDAR_CAM01'] = np.matmul(
    calib['extrinsics']['T_LIDAR_FCAMERA'], calib['extrinsics']['T_FCAMERA_FRCAMERA']); #from lidar to frontright

  calib['extrinsics']['T_LIDAR_CAM02'] = np.matmul(
    calib['extrinsics']['T_LIDAR_CAM01'], calib['extrinsics']['T_FRCAMERA_RFCAMERA']); #from lidar to front right,

  calib['extrinsics']['T_LIDAR_CAM03'] = np.matmul(
    calib['extrinsics']['T_LIDAR_CAM02'], calib['extrinsics']['T_RFCAMERA_RBCAMERA']);

  calib['extrinsics']['T_LIDAR_CAM07'] = np.matmul(
    calib['extrinsics']['T_LIDAR_FCAMERA'], np.linalg.inv(calib['extrinsics']['T_FLCAMERA_FCAMERA']));

  calib['extrinsics']['T_LIDAR_CAM06'] = np.matmul(
    calib['extrinsics']['T_LIDAR_CAM07'], np.linalg.inv(calib['extrinsics']['T_LFCAMERA_FLCAMERA']));

  calib['extrinsics']['T_LIDAR_CAM05'] = np.matmul(
    calib['extrinsics']['T_LIDAR_CAM06'], np.linalg.inv(calib['extrinsics']['T_LBCAMERA_LFCAMERA']));

  calib['extrinsics']['T_LIDAR_CAM04'] = np.matmul(
    calib['extrinsics']['T_LIDAR_CAM05'], np.linalg.inv(calib['extrinsics']['T_BCAMERA_LBCAMERA']));
  # We are not using T_RBCAMERA_BCAMERA due to the cumulative error
  '''

  #these were manually tweaked as shown in run_demo_calibration
  #0: front , 1: front right, 2: right front, 3: back right, 4: back, 5: left back, 6: left front, 7: front left

  calib['extrinsics']['T_LIDAR_CAM00'] = np.array([
    [0.03140493410305044, -0.0051327600000000044, 0.9994811341437232, 0.0063204014089569775],
    [-0.9993790343177404, 0.015076499999999998, 0.031467061677720745, -0.052515578275115334],
    [-0.015218077675811332, -0.9998609999999999, -0.004644625322140899, -0.6065496159036304],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  calib['extrinsics']['T_LIDAR_CAM01'] = np.array([
    [0.017429035748350013, 0.01775430090741544, 0.9996780312343709, -0.18634604944383004],
    [-0.9998101435901432, 0.007538145089507123, 0.017285375309904746, -0.6375628396947848],
    [-0.007216780649483202, -0.9998014285244012, 0.01789422675484401, -0.6219673001775691],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  calib['extrinsics']['T_LIDAR_CAM02'] = np.array([
    [-0.9611660208175561, -0.011165963759867425, 0.27569975389817947, -0.2196002139152005],
    [-0.2755926482030905, -0.009377814824652945, -0.9612162503319752, -0.4347723112746975],
    [0.013310369070831439, -0.9998812924723096, 0.005951200940298729, -0.4791233221725538],
    [0.0, 0.0, 0.0, 1.0, ],
  ]);

  calib['extrinsics']['T_LIDAR_CAM03'] = np.array([
    [-0.8970053026813612, 0.0061438406308544115, -0.44194897081443335, -0.9212960806673477],
    [0.4418949929699544, -0.00960549628781492, -0.8970019401798651, -0.20905184669307178],
    [-0.009772247348152243, -0.9999223945643575, 0.005906757549490006, -0.5905518072883839],
    [0.0, 0.0, 0.0, 1.0]
  ]);
  calib['extrinsics']['T_LIDAR_CAM04'] = np.array([
    [-0.05391083070903979, -0.02801224008790963, -0.9981529056783992, -0.9703750993026432],
    [0.998379786105782, 0.016697647746380866, -0.05439165923138018, -0.05777514635951181],
    [0.01819051712070557, -0.9994678822368094, 0.027066658294479656, -0.6453540010633155],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  calib['extrinsics']['T_LIDAR_CAM05'] = np.array([
    [0.8349923023269404, 0.009992749751145768, -0.5501483005778823, -0.7179096290173695],
    [0.5500976486319944, 0.006698732745195617, 0.8350590607886826, 0.5734712245063702],
    [0.01203335882371237, -0.9999151832264647, 7.98900140137711e-05, -0.6182634493285112],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  calib['extrinsics']['T_LIDAR_CAM06'] = np.array([
    [0.9431017110686303, 0.03598200715576529, 0.33051416060741984, -0.3763910925806895],
    [-0.33113248686882135, 0.012290661755638373, 0.9434914662199101, 0.44791929512142287],
    [0.029902020280154866, -0.9992641504226214, 0.023499119496881885, -0.5914170719792708],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  calib['extrinsics']['T_LIDAR_CAM07'] = np.array([
    [0.013178169291561627, 0.009230514007229166, 0.9998581329797456, 0.0023183708207018916],
    [-0.9998884526905925, -0.004944966709264369, 0.013212135974031184, 0.4620401290706413],
    [0.0050783660836566024, -0.999932592578222, 0.009176178466329636, -0.7023106181772751],
    [0.0, 0.0, 0.0, 1.0]
  ]);

  return calib;
