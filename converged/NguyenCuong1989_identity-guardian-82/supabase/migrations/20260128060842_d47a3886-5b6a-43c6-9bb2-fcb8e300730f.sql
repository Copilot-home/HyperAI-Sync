-- Enable realtime for dashboard tables
ALTER PUBLICATION supabase_realtime ADD TABLE public.entity_state;
ALTER PUBLICATION supabase_realtime ADD TABLE public.tasks;
ALTER PUBLICATION supabase_realtime ADD TABLE public.drift_events;
ALTER PUBLICATION supabase_realtime ADD TABLE public.logic_modules;
ALTER PUBLICATION supabase_realtime ADD TABLE public.sla_metrics;

-- Insert sample logic modules
INSERT INTO public.logic_modules (module_name, description, required_identity_state, is_enabled, dependencies)
VALUES 
  ('facial_landmark_encoder', 'Encodes facial landmark positions for identity preservation', 75, true, '["base_encoder"]'),
  ('voice_timbre_analyzer', 'Analyzes vocal patterns and timbre characteristics', 60, true, '["audio_processor"]'),
  ('temporal_coherence_engine', 'Ensures frame-to-frame identity consistency', 85, true, '["facial_landmark_encoder", "motion_tracker"]'),
  ('behavioral_pattern_matcher', 'Matches behavioral mannerisms and expressions', 70, true, '["pose_estimator"]'),
  ('identity_fusion_layer', 'Combines all identity signals into unified representation', 90, false, '["facial_landmark_encoder", "voice_timbre_analyzer", "behavioral_pattern_matcher"]');

-- Insert sample SLA metrics
INSERT INTO public.sla_metrics (metric_name, current_value, target_value, unit, is_compliant, last_measured_at)
VALUES 
  ('Frame Processing Rate', 28, 30, 'fps', false, now()),
  ('Identity Preservation Score', 94.5, 90, 'percent', true, now()),
  ('Drift Detection Latency', 45, 100, 'ms', true, now()),
  ('Video Output Quality', 1080, 1080, 'p', true, now()),
  ('Max Concurrent Tasks', 8, 10, 'tasks', true, now());