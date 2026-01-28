-- Create RPC function for entity initialization (called on first login)
CREATE OR REPLACE FUNCTION public.initialize_entity()
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public'
AS $$
DECLARE
  new_entity_id uuid;
  placeholder_hash char(64);
BEGIN
  -- Check if entity already exists for this user
  SELECT entity_id INTO new_entity_id
  FROM entity_identity
  WHERE owner_user_id = auth.uid();
  
  -- If exists, return the existing entity_id
  IF new_entity_id IS NOT NULL THEN
    RETURN new_entity_id;
  END IF;
  
  -- Generate placeholder hash (64 zeros - indicates NO_IDENTITY)
  placeholder_hash := repeat('0', 64);
  
  -- Create new entity_identity record
  INSERT INTO entity_identity (
    owner_user_id,
    identity_hash,
    geometry_hash,
    locked
  ) VALUES (
    auth.uid(),
    placeholder_hash,
    placeholder_hash,
    false  -- Not locked until ESTABLISHED
  )
  RETURNING entity_id INTO new_entity_id;
  
  -- identity_state is auto-created by trg_create_identity_state trigger
  -- with state = 'NO_IDENTITY', variance_score = 1.0
  
  RETURN new_entity_id;
END;
$$;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION public.initialize_entity() TO authenticated;