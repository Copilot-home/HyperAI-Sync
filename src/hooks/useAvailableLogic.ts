import { useQuery } from "@tanstack/react-query";
import { LogicRule } from "@/types/ecvm";

// Mock endpoint - in production this would be GET /v1/logic/available
async function fetchAvailableLogic(): Promise<LogicRule[]> {
  await new Promise(resolve => setTimeout(resolve, 400));
  
  return [
    {
      logic_id: "lg_face_detect",
      name: "Face Detection",
      description: "Validates presence and quality of facial features",
      available: true,
      required: true,
      category: "identity",
    },
    {
      logic_id: "lg_age_verify",
      name: "Age Verification",
      description: "Cross-references age markers with reference data",
      available: true,
      required: true,
      category: "identity",
    },
    {
      logic_id: "lg_liveness",
      name: "Liveness Check",
      description: "Anti-spoofing verification for live capture",
      available: true,
      required: false,
      category: "security",
    },
    {
      logic_id: "lg_doc_match",
      name: "Document Matching",
      description: "Validates identity against document records",
      available: false,
      required: false,
      category: "compliance",
    },
    {
      logic_id: "lg_motion_track",
      name: "Motion Tracking",
      description: "Analyzes motion patterns in video content",
      available: true,
      required: false,
      category: "video",
    },
  ];
}

export function useAvailableLogic() {
  return useQuery({
    queryKey: ["available-logic"],
    queryFn: fetchAvailableLogic,
    staleTime: 60000,
    refetchOnWindowFocus: false,
  });
}
