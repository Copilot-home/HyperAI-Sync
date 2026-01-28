import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

interface ReferenceFile {
  name: string;
  size: number;
  created_at: string;
}

interface ReferenceData {
  entity_id: string | null;
  reference_count: number;
  files: ReferenceFile[];
  identity_state: {
    state: string;
    coverage_percent: number;
    variance_score: number;
  } | null;
}

interface ProcessResult {
  entity_id: string;
  reference_count: number;
  state: string;
  coverage_percent: number;
  variance_score: number;
}

// Fetch current references and state
async function fetchReferences(): Promise<ReferenceData> {
  const { data, error } = await supabase.functions.invoke("entity-reference", {
    method: "GET",
  });

  if (error) {
    console.error("[useReferenceUpload] Fetch error:", error);
    throw new Error(error.message || "Failed to fetch references");
  }

  return data as ReferenceData;
}

// Process references after upload
async function processReferences(): Promise<ProcessResult> {
  const { data, error } = await supabase.functions.invoke("entity-reference", {
    method: "POST",
  });

  if (error) {
    console.error("[useReferenceUpload] Process error:", error);
    throw new Error(error.message || "Failed to process references");
  }

  return data as ProcessResult;
}

// Upload a file to storage
async function uploadReferenceFile(file: File): Promise<string> {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  const fileExt = file.name.split(".").pop()?.toLowerCase();
  const fileName = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}.${fileExt}`;
  const filePath = `${user.id}/${fileName}`;

  const { error } = await supabase.storage
    .from("entity-references")
    .upload(filePath, file, {
      cacheControl: "3600",
      upsert: false,
    });

  if (error) {
    console.error("[useReferenceUpload] Upload error:", error);
    throw new Error(error.message || "Failed to upload file");
  }

  return filePath;
}

export function useReferences() {
  return useQuery({
    queryKey: ["entity-references"],
    queryFn: fetchReferences,
    staleTime: 30000,
    retry: false, // ECVM: fail-closed
  });
}

export function useUploadReference() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (files: File[]) => {
      // Upload all files
      const uploadPromises = files.map(file => uploadReferenceFile(file));
      await Promise.all(uploadPromises);

      // Process references to update identity state
      const result = await processReferences();
      return result;
    },
    onSuccess: () => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ["entity-references"] });
      queryClient.invalidateQueries({ queryKey: ["entity-state"] });
    },
  });
}

export function useDeleteReference() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (fileName: string) => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error("Not authenticated");

      const filePath = `${user.id}/${fileName}`;
      const { error } = await supabase.storage
        .from("entity-references")
        .remove([filePath]);

      if (error) throw new Error(error.message);

      // Reprocess to update identity state
      return await processReferences();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entity-references"] });
      queryClient.invalidateQueries({ queryKey: ["entity-state"] });
    },
  });
}
