-- Enable realtime for identity_state table to allow live coverage % updates
ALTER PUBLICATION supabase_realtime ADD TABLE public.identity_state;