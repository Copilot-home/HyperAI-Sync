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
      audit_log: {
        Row: {
          action: string
          actor_id: string
          actor_type: string
          details: Json
          id: string
          resource_id: string
          resource_type: string
          timestamp: string
        }
        Insert: {
          action: string
          actor_id: string
          actor_type: string
          details?: Json
          id?: string
          resource_id: string
          resource_type: string
          timestamp?: string
        }
        Update: {
          action?: string
          actor_id?: string
          actor_type?: string
          details?: Json
          id?: string
          resource_id?: string
          resource_type?: string
          timestamp?: string
        }
        Relationships: []
      }
      drift_event: {
        Row: {
          acknowledged: boolean
          baseline: number
          current_value: number
          detected_at: string
          drift_id: string
          drift_type: Database["public"]["Enums"]["drift_type_enum"]
          entity_id: string | null
          logic_id: string | null
          severity: number
        }
        Insert: {
          acknowledged?: boolean
          baseline?: number
          current_value?: number
          detected_at?: string
          drift_id?: string
          drift_type: Database["public"]["Enums"]["drift_type_enum"]
          entity_id?: string | null
          logic_id?: string | null
          severity: number
        }
        Update: {
          acknowledged?: boolean
          baseline?: number
          current_value?: number
          detected_at?: string
          drift_id?: string
          drift_type?: Database["public"]["Enums"]["drift_type_enum"]
          entity_id?: string | null
          logic_id?: string | null
          severity?: number
        }
        Relationships: [
          {
            foreignKeyName: "drift_event_entity_id_fkey"
            columns: ["entity_id"]
            isOneToOne: false
            referencedRelation: "entity_identity"
            referencedColumns: ["entity_id"]
          },
          {
            foreignKeyName: "drift_event_logic_id_fkey"
            columns: ["logic_id"]
            isOneToOne: false
            referencedRelation: "logic_module"
            referencedColumns: ["logic_id"]
          },
        ]
      }
      entity_identity: {
        Row: {
          created_at: string
          entity_id: string
          geometry_hash: string
          identity_hash: string
          locked: boolean
          owner_user_id: string
        }
        Insert: {
          created_at?: string
          entity_id?: string
          geometry_hash: string
          identity_hash: string
          locked?: boolean
          owner_user_id: string
        }
        Update: {
          created_at?: string
          entity_id?: string
          geometry_hash?: string
          identity_hash?: string
          locked?: boolean
          owner_user_id?: string
        }
        Relationships: []
      }
      identity_state: {
        Row: {
          coverage_percent: number
          entity_id: string
          state: Database["public"]["Enums"]["identity_state_enum"]
          updated_at: string
          variance_score: number
        }
        Insert: {
          coverage_percent?: number
          entity_id: string
          state?: Database["public"]["Enums"]["identity_state_enum"]
          updated_at?: string
          variance_score?: number
        }
        Update: {
          coverage_percent?: number
          entity_id?: string
          state?: Database["public"]["Enums"]["identity_state_enum"]
          updated_at?: string
          variance_score?: number
        }
        Relationships: [
          {
            foreignKeyName: "identity_state_entity_id_fkey"
            columns: ["entity_id"]
            isOneToOne: true
            referencedRelation: "entity_identity"
            referencedColumns: ["entity_id"]
          },
        ]
      }
      logic_module: {
        Row: {
          camera_profile: Json
          created_at: string
          description: string | null
          drift_risk_score: number
          enabled: boolean
          logic_id: string
          motion_profile: Json
          name: string
          required_identity_state: Database["public"]["Enums"]["identity_state_enum"]
          task_type: Database["public"]["Enums"]["task_type_enum"]
          updated_at: string
          version: number
        }
        Insert: {
          camera_profile?: Json
          created_at?: string
          description?: string | null
          drift_risk_score?: number
          enabled?: boolean
          logic_id?: string
          motion_profile?: Json
          name: string
          required_identity_state?: Database["public"]["Enums"]["identity_state_enum"]
          task_type: Database["public"]["Enums"]["task_type_enum"]
          updated_at?: string
          version?: number
        }
        Update: {
          camera_profile?: Json
          created_at?: string
          description?: string | null
          drift_risk_score?: number
          enabled?: boolean
          logic_id?: string
          motion_profile?: Json
          name?: string
          required_identity_state?: Database["public"]["Enums"]["identity_state_enum"]
          task_type?: Database["public"]["Enums"]["task_type_enum"]
          updated_at?: string
          version?: number
        }
        Relationships: []
      }
      logic_version_history: {
        Row: {
          changed_at: string
          changed_by: string | null
          logic_id: string
          snapshot: Json
          version: number
        }
        Insert: {
          changed_at?: string
          changed_by?: string | null
          logic_id: string
          snapshot: Json
          version: number
        }
        Update: {
          changed_at?: string
          changed_by?: string | null
          logic_id?: string
          snapshot?: Json
          version?: number
        }
        Relationships: [
          {
            foreignKeyName: "logic_version_history_logic_id_fkey"
            columns: ["logic_id"]
            isOneToOne: false
            referencedRelation: "logic_module"
            referencedColumns: ["logic_id"]
          },
        ]
      }
      task_execution_log: {
        Row: {
          entity_id: string
          executed_at: string
          execution_time_ms: number
          logic_applied: string[]
          logic_id: string | null
          metadata: Json
          task_id: string
          task_type: Database["public"]["Enums"]["task_type_enum"]
          verdict: Database["public"]["Enums"]["kernel_verdict_enum"]
        }
        Insert: {
          entity_id: string
          executed_at?: string
          execution_time_ms?: number
          logic_applied?: string[]
          logic_id?: string | null
          metadata?: Json
          task_id?: string
          task_type: Database["public"]["Enums"]["task_type_enum"]
          verdict: Database["public"]["Enums"]["kernel_verdict_enum"]
        }
        Update: {
          entity_id?: string
          executed_at?: string
          execution_time_ms?: number
          logic_applied?: string[]
          logic_id?: string | null
          metadata?: Json
          task_id?: string
          task_type?: Database["public"]["Enums"]["task_type_enum"]
          verdict?: Database["public"]["Enums"]["kernel_verdict_enum"]
        }
        Relationships: [
          {
            foreignKeyName: "task_execution_log_entity_id_fkey"
            columns: ["entity_id"]
            isOneToOne: false
            referencedRelation: "entity_identity"
            referencedColumns: ["entity_id"]
          },
          {
            foreignKeyName: "task_execution_log_logic_id_fkey"
            columns: ["logic_id"]
            isOneToOne: false
            referencedRelation: "logic_module"
            referencedColumns: ["logic_id"]
          },
        ]
      }
      unmet_logic_signal: {
        Row: {
          created_at: string
          entity_id: string
          observed_state: Database["public"]["Enums"]["identity_state_enum"]
          reason: string | null
          requested_task: Database["public"]["Enums"]["task_type_enum"]
          severity: string
          signal_id: string
        }
        Insert: {
          created_at?: string
          entity_id: string
          observed_state: Database["public"]["Enums"]["identity_state_enum"]
          reason?: string | null
          requested_task: Database["public"]["Enums"]["task_type_enum"]
          severity?: string
          signal_id?: string
        }
        Update: {
          created_at?: string
          entity_id?: string
          observed_state?: Database["public"]["Enums"]["identity_state_enum"]
          reason?: string | null
          requested_task?: Database["public"]["Enums"]["task_type_enum"]
          severity?: string
          signal_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "unmet_logic_signal_entity_id_fkey"
            columns: ["entity_id"]
            isOneToOne: false
            referencedRelation: "entity_identity"
            referencedColumns: ["entity_id"]
          },
        ]
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
      initialize_entity: { Args: never; Returns: string }
    }
    Enums: {
      app_role: "admin" | "user"
      drift_type_enum: "PER_NODE" | "SYSTEMIC"
      identity_state_enum:
        | "NO_IDENTITY"
        | "INSUFFICIENT"
        | "ESTABLISHED"
        | "DRIFT"
      kernel_verdict_enum: "PASS" | "REJECT" | "HALT"
      task_type_enum: "image_static" | "image" | "video" | "validation"
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
      drift_type_enum: ["PER_NODE", "SYSTEMIC"],
      identity_state_enum: [
        "NO_IDENTITY",
        "INSUFFICIENT",
        "ESTABLISHED",
        "DRIFT",
      ],
      kernel_verdict_enum: ["PASS", "REJECT", "HALT"],
      task_type_enum: ["image_static", "image", "video", "validation"],
    },
  },
} as const
