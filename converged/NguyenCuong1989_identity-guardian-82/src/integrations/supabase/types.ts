export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.1"
  }
  public: {
    Tables: {
      drift_events: {
        Row: {
          created_at: string
          description: string | null
          event_type: string
          id: string
          metadata: Json | null
          node_id: string | null
          resolved: boolean | null
          resolved_at: string | null
          scope: Database["public"]["Enums"]["drift_scope"]
          severity: number | null
        }
        Insert: {
          created_at?: string
          description?: string | null
          event_type: string
          id?: string
          metadata?: Json | null
          node_id?: string | null
          resolved?: boolean | null
          resolved_at?: string | null
          scope?: Database["public"]["Enums"]["drift_scope"]
          severity?: number | null
        }
        Update: {
          created_at?: string
          description?: string | null
          event_type?: string
          id?: string
          metadata?: Json | null
          node_id?: string | null
          resolved?: boolean | null
          resolved_at?: string | null
          scope?: Database["public"]["Enums"]["drift_scope"]
          severity?: number | null
        }
        Relationships: []
      }
      entity_state: {
        Row: {
          axes_state: Json | null
          created_at: string
          id: string
          identity_coverage: number
          landmark_coverage: Json | null
          locked: boolean | null
          node_id: string
          updated_at: string
          user_id: string
        }
        Insert: {
          axes_state?: Json | null
          created_at?: string
          id?: string
          identity_coverage?: number
          landmark_coverage?: Json | null
          locked?: boolean | null
          node_id: string
          updated_at?: string
          user_id: string
        }
        Update: {
          axes_state?: Json | null
          created_at?: string
          id?: string
          identity_coverage?: number
          landmark_coverage?: Json | null
          locked?: boolean | null
          node_id?: string
          updated_at?: string
          user_id?: string
        }
        Relationships: []
      }
      logic_modules: {
        Row: {
          created_at: string
          dependencies: Json | null
          description: string | null
          id: string
          is_enabled: boolean | null
          module_name: string
          required_identity_state: number | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          dependencies?: Json | null
          description?: string | null
          id?: string
          is_enabled?: boolean | null
          module_name: string
          required_identity_state?: number | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          dependencies?: Json | null
          description?: string | null
          id?: string
          is_enabled?: boolean | null
          module_name?: string
          required_identity_state?: number | null
          updated_at?: string
        }
        Relationships: []
      }
      sla_metrics: {
        Row: {
          created_at: string
          current_value: number
          id: string
          is_compliant: boolean | null
          last_measured_at: string | null
          metric_name: string
          target_value: number
          unit: string | null
        }
        Insert: {
          created_at?: string
          current_value?: number
          id?: string
          is_compliant?: boolean | null
          last_measured_at?: string | null
          metric_name: string
          target_value: number
          unit?: string | null
        }
        Update: {
          created_at?: string
          current_value?: number
          id?: string
          is_compliant?: boolean | null
          last_measured_at?: string | null
          metric_name?: string
          target_value?: number
          unit?: string | null
        }
        Relationships: []
      }
      tasks: {
        Row: {
          completed_at: string | null
          created_at: string
          frame_count: number | null
          halt_point: number | null
          halt_reason: string | null
          id: string
          progress: number | null
          started_at: string | null
          status: Database["public"]["Enums"]["task_status"]
          task_name: string
          updated_at: string
          user_id: string | null
          verdict: Database["public"]["Enums"]["verdict_type"] | null
        }
        Insert: {
          completed_at?: string | null
          created_at?: string
          frame_count?: number | null
          halt_point?: number | null
          halt_reason?: string | null
          id?: string
          progress?: number | null
          started_at?: string | null
          status?: Database["public"]["Enums"]["task_status"]
          task_name: string
          updated_at?: string
          user_id?: string | null
          verdict?: Database["public"]["Enums"]["verdict_type"] | null
        }
        Update: {
          completed_at?: string | null
          created_at?: string
          frame_count?: number | null
          halt_point?: number | null
          halt_reason?: string | null
          id?: string
          progress?: number | null
          started_at?: string | null
          status?: Database["public"]["Enums"]["task_status"]
          task_name?: string
          updated_at?: string
          user_id?: string | null
          verdict?: Database["public"]["Enums"]["verdict_type"] | null
        }
        Relationships: []
      }
      user_roles: {
        Row: {
          created_at: string
          id: string
          role: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Insert: {
          created_at?: string
          id?: string
          role?: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Update: {
          created_at?: string
          id?: string
          role?: Database["public"]["Enums"]["app_role"]
          user_id?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      has_role: {
        Args: {
          _role: Database["public"]["Enums"]["app_role"]
          _user_id: string
        }
        Returns: boolean
      }
    }
    Enums: {
      app_role: "admin" | "user"
      drift_scope: "per_node" | "systemic"
      task_status: "queued" | "running" | "halting" | "completed"
      verdict_type: "PASS" | "REJECT" | "HALT"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      app_role: ["admin", "user"],
      drift_scope: ["per_node", "systemic"],
      task_status: ["queued", "running", "halting", "completed"],
      verdict_type: ["PASS", "REJECT", "HALT"],
    },
  },
} as const
