#!/bin/bash

# Advanced Sequential Job Submission with Completion Waiting
# This script submits jobs and waits for each to complete before submitting the next
# Use this if you want truly sequential execution (each job fully completes before next starts)

set -e

WKDIR="/sc/arion/work/cheny69/1216"
LOG_DIR="${WKDIR}/submission_logs"
SUBMISSION_START=$(date '+%Y-%m-%d_%H-%M-%S')

# Create log directory
mkdir -p ${LOG_DIR}

echo "=========================================="
echo "HER2 Boltz Sequential Job Submission"
echo "(Waiting for Each Job Completion)"
echo "=========================================="
echo "Working Directory: ${WKDIR}"
echo "Log Directory: ${LOG_DIR}"
echo "Submission Start: ${SUBMISSION_START}"
echo ""

# Array of all jobs in submission order
declare -a JOBS=(
    # Monomer/ECD predictions
    "d16"
    "WT_ECD"
    "S310F"
    
    # Monomer/ICD predictions
    "WT_ICD"
    "K753E"
    "L755S"
    
    # Multimer/dimer predictions
    "WT_dimer"
    "d16_dimer"
    
    # Multimer/drug-binding predictions (trastuzumab)
    "WT_trastuzumab"
    "d16_trastuzumab"
    
    # Multimer/drug-binding predictions (pertuzumab)
    "WT_pertuzumab"
    "S310F_pertuzumab"
    
    # Multimer/drug-binding predictions (lapatinib)
    "WT_lapatinib"
    "K753E_lapatinib"
    "L755S_lapatinib"
)

TOTAL_JOBS=${#JOBS[@]}
echo "Total jobs to submit: ${TOTAL_JOBS}"
echo ""

# Change to working directory
cd ${WKDIR}

# Track results
SUCCEEDED=0
FAILED=0
SUBMISSION_LOG="${LOG_DIR}/submissions_advanced_${SUBMISSION_START}.log"

{
    echo "Advanced Sequential Submission Log"
    echo "Started: $(date)"
    echo ""
} > ${SUBMISSION_LOG}

# Submit each job sequentially
for ((i=0; i<${TOTAL_JOBS}; i++)); do
    JOB=${JOBS[$i]}
    JOB_NUM=$((i+1))
    
    echo "[${JOB_NUM}/${TOTAL_JOBS}] Processing ${JOB}..."
    
    if [ -f "${JOB}.lsf" ] && [ -f "${JOB}.yaml" ]; then
        # Submit the job
        echo "  Submitting..."
        JOB_ID=$(bsub < ${JOB}.lsf 2>&1 | grep -oP 'Job <\K[0-9]+')
        
        if [ ! -z "$JOB_ID" ]; then
            echo "  ✓ Job ID: ${JOB_ID}"
            {
                echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: Job ID ${JOB_ID} submitted at $(date)"
            } >> ${SUBMISSION_LOG}
            
            # Wait for this job to complete
            echo "  Waiting for Job ${JOB_ID} to complete..."
            while true; do
                JOB_STATUS=$(bjobs ${JOB_ID} 2>/dev/null | tail -1 | awk '{print $3}')
                
                if [ -z "$JOB_STATUS" ]; then
                    # Job no longer in queue - it's done
                    echo "  ✓ Job ${JOB_ID} completed"
                    {
                        echo "  ${JOB}: Job completed at $(date)"
                    } >> ${SUBMISSION_LOG}
                    SUCCEEDED=$((SUCCEEDED+1))
                    break
                elif [ "$JOB_STATUS" = "RUN" ] || [ "$JOB_STATUS" = "PEND" ]; then
                    # Still running or pending
                    echo "  Status: $JOB_STATUS - checking again in 30 seconds..."
                    sleep 30
                else
                    # Job finished (could be done, failed, etc.)
                    echo "  ✓ Job finished with status: $JOB_STATUS"
                    {
                        echo "  ${JOB}: Job finished with status ${JOB_STATUS} at $(date)"
                    } >> ${SUBMISSION_LOG}
                    SUCCEEDED=$((SUCCEEDED+1))
                    break
                fi
            done
            
        else
            echo "  ✗ Failed to submit ${JOB}"
            {
                echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: FAILED at $(date)"
            } >> ${SUBMISSION_LOG}
            FAILED=$((FAILED+1))
        fi
    else
        echo "  ✗ Missing files: ${JOB}.lsf or ${JOB}.yaml"
        {
            echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: MISSING FILES at $(date)"
        } >> ${SUBMISSION_LOG}
        FAILED=$((FAILED+1))
    fi
    
    echo ""
done

# Print summary
echo "=========================================="
echo "Submission Summary"
echo "=========================================="
echo "Total jobs submitted: ${SUCCEEDED}"
echo "Total jobs failed: ${FAILED}"
echo "Submission End: $(date)"
echo ""
echo "Submission Log: ${SUBMISSION_LOG}"
echo ""
echo "To check final results:"
echo "  ls -la ${WKDIR}/results/"
echo ""

# Append summary to log
{
    echo ""
    echo "Completed: $(date)"
    echo "Succeeded: ${SUCCEEDED}"
    echo "Failed: ${FAILED}"
} >> ${SUBMISSION_LOG}

exit 0
