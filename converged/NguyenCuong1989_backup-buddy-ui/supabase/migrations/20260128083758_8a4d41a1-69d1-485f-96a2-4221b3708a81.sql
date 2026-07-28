-- Create storage bucket for entity reference images
INSERT INTO storage.buckets (id, name, public)
VALUES ('entity-references', 'entity-references', false)
ON CONFLICT (id) DO NOTHING;

-- RLS: Users can upload to their own entity folder
CREATE POLICY "Users can upload their own references"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'entity-references' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- RLS: Users can view their own references
CREATE POLICY "Users can view their own references"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'entity-references' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- RLS: Users can delete their own references
CREATE POLICY "Users can delete their own references"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'entity-references' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Add reference_count to identity_state for tracking
ALTER TABLE public.identity_state 
ADD COLUMN IF NOT EXISTS coverage_percent float NOT NULL DEFAULT 0;

-- Ensure reference_uploaded flag exists on some view
-- We'll track this via edge function logic based on storage contents