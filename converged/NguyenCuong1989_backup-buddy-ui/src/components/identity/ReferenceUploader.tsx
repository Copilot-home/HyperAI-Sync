import { useState, useCallback } from "react";
import { Upload, X, Image, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useUploadReference, useReferences, useDeleteReference } from "@/hooks/useReferenceUpload";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export function ReferenceUploader() {
  const [dragActive, setDragActive] = useState(false);
  const { data: references, isLoading: loadingRefs } = useReferences();
  const uploadMutation = useUploadReference();
  const deleteMutation = useDeleteReference();

  const validateFiles = useCallback((files: File[]): File[] => {
    return files.filter(file => {
      if (!ALLOWED_TYPES.includes(file.type)) {
        toast.error(`Invalid file type: ${file.name}. Use JPG, PNG, or WebP.`);
        return false;
      }
      if (file.size > MAX_FILE_SIZE) {
        toast.error(`File too large: ${file.name}. Max 10MB.`);
        return false;
      }
      return true;
    });
  }, []);

  const handleUpload = useCallback(async (files: File[]) => {
    const validFiles = validateFiles(files);
    if (validFiles.length === 0) return;

    try {
      await uploadMutation.mutateAsync(validFiles);
      toast.success(`Uploaded ${validFiles.length} reference(s)`);
    } catch (error) {
      toast.error(`Upload failed: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }, [validateFiles, uploadMutation]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    handleUpload(files);
  }, [handleUpload]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      handleUpload(files);
    }
  }, [handleUpload]);

  const handleDelete = useCallback(async (fileName: string) => {
    try {
      await deleteMutation.mutateAsync(fileName);
      toast.success("Reference deleted");
    } catch (error) {
      toast.error(`Delete failed: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }, [deleteMutation]);

  const isUploading = uploadMutation.isPending;
  const isDeleting = deleteMutation.isPending;

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        className={cn(
          "relative border-2 border-dashed rounded-lg p-6 transition-colors",
          dragActive 
            ? "border-primary bg-primary/5" 
            : "border-border hover:border-primary/50",
          isUploading && "pointer-events-none opacity-50"
        )}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple
          accept={ALLOWED_TYPES.join(",")}
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={isUploading}
        />
        
        <div className="flex flex-col items-center gap-2 text-center">
          {isUploading ? (
            <>
              <Loader2 className="h-8 w-8 text-primary animate-spin" />
              <p className="text-sm text-muted-foreground font-mono">
                Uploading...
              </p>
            </>
          ) : (
            <>
              <Upload className="h-8 w-8 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-muted-foreground font-mono">
                JPG, PNG, WebP up to 10MB
              </p>
            </>
          )}
        </div>
      </div>

      {/* File List */}
      {loadingRefs ? (
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="h-4 w-4 animate-spin" />
          <span className="font-mono text-sm">Loading references...</span>
        </div>
      ) : references && references.files.length > 0 ? (
        <div className="space-y-2">
          <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider">
            Uploaded References ({references.reference_count})
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            {references.files.map((file) => (
              <div
                key={file.name}
                className="relative group bg-muted rounded-lg p-2 flex items-center gap-2"
              >
                <Image className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <span className="text-xs font-mono truncate flex-1">
                  {file.name}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => handleDelete(file.name)}
                  disabled={isDeleting}
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="flex items-center gap-2 text-muted-foreground bg-muted/50 rounded-lg p-3">
          <AlertCircle className="h-4 w-4" />
          <span className="text-sm">
            No reference images uploaded. Upload at least 10 images for ESTABLISHED identity.
          </span>
        </div>
      )}

      {/* Requirements Info */}
      <div className="text-xs font-mono text-muted-foreground space-y-1 border-t pt-3">
        <div>• 0 images → NO_IDENTITY</div>
        <div>• 1-9 images → INSUFFICIENT</div>
        <div>• 10+ images → ESTABLISHED</div>
      </div>
    </div>
  );
}
