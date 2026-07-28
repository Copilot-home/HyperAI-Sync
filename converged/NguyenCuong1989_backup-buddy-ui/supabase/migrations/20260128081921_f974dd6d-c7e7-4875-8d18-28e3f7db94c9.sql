-- Seed Logic Bank with test logic modules
-- ECVM-CS-1.0 compliant seed data

-- Insert sample logic modules for testing Generate page
INSERT INTO public.logic_module (
  logic_id,
  name,
  description,
  task_type,
  required_identity_state,
  camera_profile,
  motion_profile,
  drift_risk_score,
  enabled,
  version
) VALUES
  (
    '11111111-1111-1111-1111-111111111111',
    'Static Portrait',
    'Generate static portrait images with strict identity preservation',
    'image_static',
    'ESTABLISHED',
    '{"fov": 50, "distance": 1.2, "angle_range": [-15, 15]}',
    '{}',
    0.15,
    true,
    1
  ),
  (
    '22222222-2222-2222-2222-222222222222',
    'Dynamic Portrait',
    'Generate portrait images with moderate pose variation',
    'image',
    'ESTABLISHED',
    '{"fov": 60, "distance": 1.5, "angle_range": [-30, 30]}',
    '{"rotation_limit": 10}',
    0.25,
    true,
    1
  ),
  (
    '33333333-3333-3333-3333-333333333333',
    'Video Sequence',
    'Generate video sequences with temporal consistency',
    'video',
    'ESTABLISHED',
    '{"fov": 55, "distance": 1.8, "angle_range": [-45, 45]}',
    '{"frame_rate": 30, "duration_max": 10, "motion_blur": false}',
    0.35,
    true,
    1
  ),
  (
    '44444444-4444-4444-4444-444444444444',
    'Identity Validation',
    'Validate identity consistency across reference set',
    'validation',
    'INSUFFICIENT',
    '{}',
    '{}',
    0.10,
    true,
    1
  ),
  (
    '55555555-5555-5555-5555-555555555555',
    'High-Risk Video (Disabled)',
    'Experimental video generation with high drift risk',
    'video',
    'ESTABLISHED',
    '{"fov": 70, "distance": 2.5, "angle_range": [-60, 60]}',
    '{"frame_rate": 60, "duration_max": 30, "motion_blur": true}',
    0.65,
    false,
    1
  )
ON CONFLICT (logic_id) DO NOTHING;