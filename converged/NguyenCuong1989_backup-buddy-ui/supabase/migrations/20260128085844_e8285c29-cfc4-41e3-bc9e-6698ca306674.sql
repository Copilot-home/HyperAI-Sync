
-- Fix: Allow identity update only when transitioning FROM placeholder hash TO real hash (one-time only)
-- After the first real hash is set, identity becomes truly immutable

CREATE OR REPLACE FUNCTION public.forbid_identity_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  placeholder_hash char(64);
BEGIN
  placeholder_hash := repeat('0', 64);
  
  -- Allow transition from placeholder to real hash (first and only valid update)
  IF OLD.identity_hash = placeholder_hash AND NEW.identity_hash != placeholder_hash THEN
    RETURN NEW;
  END IF;
  
  -- Block all other updates
  RAISE EXCEPTION 'IDENTITY_IMMUTABLE: Cannot modify identity records after establishment';
END;
$$;

-- Recreate trigger to ensure it's properly attached
DROP TRIGGER IF EXISTS trg_forbid_identity_update ON entity_identity;

CREATE TRIGGER trg_forbid_identity_update
  BEFORE UPDATE ON entity_identity
  FOR EACH ROW
  EXECUTE FUNCTION forbid_identity_update();

-- Also ensure delete is still blocked
CREATE OR REPLACE FUNCTION public.forbid_identity_delete()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  RAISE EXCEPTION 'IDENTITY_IMMUTABLE: Cannot delete identity records';
END;
$$;

DROP TRIGGER IF EXISTS trg_forbid_identity_delete ON entity_identity;

CREATE TRIGGER trg_forbid_identity_delete
  BEFORE DELETE ON entity_identity
  FOR EACH ROW
  EXECUTE FUNCTION forbid_identity_delete();
