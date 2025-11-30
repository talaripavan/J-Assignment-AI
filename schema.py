"""Profile classification schema used for structured metadata extraction."""

from typing import Optional, List , Literal
from enum import Enum
from pydantic import BaseModel, Field, model_validator

class ResumeValidationResult(BaseModel):
    """ Resume Routerclear """
    is_resume: bool
    reason: str
    confidence: Optional[Literal["high", "medium", "low"]] = None

class RoleType(str, Enum):
    """Enumeration representing the classification of a profile."""
    TECH = "TECH"
    NON_TECH = "NON_TECH"
    UNKNOWN = "UNKNOWN"


class ContactInfo(BaseModel):
    """
    Contact information extracted from the source profile.

    Attributes:
        email (EmailStr): Validated email address.
        phone (str): Raw phone number string. Can be normalized upstream.
    """
    email: str
    phone: str


class Profile(BaseModel):
    """
    Structured representation of a classified profile.

    This model includes:
        - Classification metadata (role type + confidence score)
        - Contact information (always required)
        - Conditional technical attributes (only for TECH profiles)

    Validation rules:
        - TECH profiles must include years_of_experience, technical_skills,
          and a generated or extracted 2-sentence summary.
        - NON_TECH profiles must NOT contain any TECH-specific fields.
    """

    # ----- Classification Metadata -----
    role_type: RoleType = Field(
        ...,
        description="Classification result for the profile: TECH, NON_TECH, or UNKNOWN."
    )

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="System confidence score for classification (0.0-1.0)."
    )

    # ----- Contact Info (always required) -----
    contact_info: ContactInfo

    # ----- Tech-only Fields -----
    years_of_experience: Optional[float] = Field(
        default=None,
        description="Estimated years of experience (TECH only)."
    )

    technical_skills: Optional[List[str]] = Field(
        default=None,
        description="List of extracted or inferred technical skills (TECH only)."
    )

    summary: Optional[str] = Field(
        default=None,
        description="Two-sentence summary of the candidate (TECH only)."
    )

    @model_validator(mode="after")
    def validate_role_fields(self):
        """
        Soft-validation for agent-friendly structured output.

        - Never raises exceptions.
        - Missing TECH fields are replaced with guidance messages.
        - Missing contact_info is initialized with message placeholders.
        - NON-TECH fields are cleared silently.
        """

        # ---------- Ensure contact_info exists ----------
        if self.contact_info is None:
            self.contact_info = ContactInfo(
                email="MISSING_FIELD: Please provide a valid email.",
                phone="MISSING_FIELD: Please provide a phone number."
            )
        else:
            if not self.contact_info.email:
                self.contact_info.email = "MISSING_FIELD: Please provide a valid email."
            if not self.contact_info.phone:
                self.contact_info.phone = "MISSING_FIELD: Please provide a phone number."

        # ---------- TECH ----------
        if self.role_type == RoleType.TECH:

            # years_of_experience: optional float, using string message for missing
            if self.years_of_experience is None:
                self.years_of_experience = "MISSING_FIELD: Please provide estimated years_of_experience."

            if self.technical_skills is None:
                self.technical_skills = ["MISSING_FIELD: Please provide technical_skills."]

            if not self.summary:
                self.summary = "MISSING_FIELD: Please provide a 2-sentence technical summary."

        # ---------- NON-TECH ----------
        if self.role_type == RoleType.NON_TECH:
            # Remove TECH-only fields silently
            self.years_of_experience = None
            self.technical_skills = None
            self.summary = None

        return self


'''
    # ---------- CONDITIONAL VALIDATION ----------
    @model_validator(mode="after")
    def validate_role_fields(self):
        """
        Validate that fields align with the detected role type.

        Rules enforced:
            - TECH profiles must include technical fields.
            - NON_TECH profiles must not contain any TECH-only fields.
        """
        if self.role_type == RoleType.TECH:
            if self.years_of_experience is None:
                raise ValueError("TECH profiles require 'years_of_experience'.")

            if self.technical_skills is None:
                raise ValueError("TECH profiles require 'technical_skills'.")

            if not self.summary:
                raise ValueError(
                    "TECH profiles require a 2-sentence 'summary'."
                )

        if self.role_type == RoleType.NON_TECH:
            if any([self.years_of_experience, self.technical_skills, self.summary]):
                raise ValueError(
                    "NON_TECH profiles must not include TECH-specific fields: "
                    "'years_of_experience', 'technical_skills', or 'summary'."
                )

        return self
'''